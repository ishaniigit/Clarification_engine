
import json
import re
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
schema_path = project_root / "data" / "spider" / "tables.json"

with open(schema_path, "r", encoding="utf-8") as f:
    schemas = json.load(f)


COLUMN_SYNONYMS = {
    "name": {"names", "individual", "individuals"},
    "country": {"nation", "nations", "india"},
    "location": {"place", "places", "where"},
    "date": {"when", "day"},
    "year": {"years"},
    "killed": {"deaths", "fatalities"},
    "injured": {"wounded", "injuries"},
    "home town": {"hometown", "city"},
}

GENERIC_WORDS = {"people", "person", "id"}


def tokenize(text):
    return set(re.findall(r"[a-zA-Z0-9]+", text.lower()))


def get_schema(db_id):
    for schema in schemas:
        if schema["db_id"] == db_id:
            return schema
    return None


def score_column(column_name, question_words):
    column_words = tokenize(column_name)
    useful_words = column_words - GENERIC_WORDS

    aliases = COLUMN_SYNONYMS.get(column_name.lower(), set())
    alias_words = set()

    for alias in aliases:
        alias_words.update(tokenize(alias))

    if useful_words & question_words:
        return 1.0

    if alias_words & question_words:
        return 0.8

    return 0.0


def link_question_to_schema(question, db_id):
    schema = get_schema(db_id)

    if schema is None:
        return {"error": f"Database '{db_id}' not found"}

    question_words = tokenize(question)
    tables = schema["table_names"]
    columns = schema["column_names"]

    direct_matches = []
    matched_tables = set()
    match_reasons = {}
    relevance_scores = {}

    for table_index, column_name in columns:
        if table_index == -1:
            continue

        table_name = tables[table_index]
        full_name = f"{table_name}.{column_name}"

        score = score_column(column_name, question_words)

        if score > 0:
            direct_matches.append(full_name)
            matched_tables.add(table_name)
            relevance_scores[full_name] = score

            column_words = tokenize(column_name)
            aliases = COLUMN_SYNONYMS.get(
                column_name.lower(), set()
            )
            alias_words = set()

            for alias in aliases:
                alias_words.update(tokenize(alias))

            matched_words = (
                (column_words - GENERIC_WORDS) | alias_words
            ) & question_words

            match_reasons[full_name] = sorted(matched_words)

    direct_matches.sort(
        key=lambda name: relevance_scores[name],
        reverse=True
    )

    join_columns = []

    if len(matched_tables) > 1:
        for left_index, right_index in schema["foreign_keys"]:
            left_table_index, left_column = columns[left_index]
            right_table_index, right_column = columns[right_index]

            left_table = tables[left_table_index]
            right_table = tables[right_table_index]

            if (
                left_table in matched_tables
                and right_table in matched_tables
            ):
                for table_name, column_name in [
                    (left_table, left_column),
                    (right_table, right_column),
                ]:
                    full_name = f"{table_name}.{column_name}"

                    if (
                        full_name not in direct_matches
                        and full_name not in join_columns
                    ):
                        join_columns.append(full_name)

    return {
        "question": question,
        "tables": sorted(matched_tables),
        "direct_matches": direct_matches,
        "relevance_scores": relevance_scores,
        "join_columns": join_columns,
        "match_reasons": match_reasons,
    }

if __name__ == "__main__":
    question = "Show the names of people who were injured in India."

    result = link_question_to_schema(question, "perpetrator")

    print(json.dumps(result, indent=4))
