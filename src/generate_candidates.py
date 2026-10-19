
import json
import re

from schema_link import link_question_to_schema
from find_join_paths import find_join_paths, get_schema


def quote_identifier(name):
    return '"' + name.replace('"', '""') + '"'


def generate_candidates(question, db_id):
    schema = get_schema(db_id)

    if schema is None:
        return {"error": f"Database '{db_id}' not found"}

    links = link_question_to_schema(question, db_id)

    if "error" in links:
        return links

    direct_matches = links["direct_matches"]
    matched_tables = links["tables"]

    join_info = find_join_paths(schema, matched_tables)

    required_tables = join_info["required_tables"]
    relationships = join_info["join_relationships"]

    selected_column = None

    for column in direct_matches:
        table, column_name = column.split(".", 1)

        if column_name.lower() in {"name", "names"}:
            selected_column = (table, column_name)
            break

    if selected_column is None:
        return {
            "question": question,
            "message": "No supported SELECT column identified yet.",
            "schema_links": links,
        }

    select_table, select_column = selected_column
    sql = (
        f"SELECT DISTINCT {quote_identifier(select_table)}."
        f"{quote_identifier(select_column)}"
    )

    first_table = required_tables[0]
    sql += f"\nFROM {quote_identifier(first_table)}"

    joined_tables = {first_table}

    while joined_tables != set(required_tables):
        added_table = False

        for relationship in relationships:
            left = relationship["left_table"]
            right = relationship["right_table"]

            if left in joined_tables and right not in joined_tables:
                sql += (
                    f"\nJOIN {quote_identifier(right)}"
                    f"\n  ON {quote_identifier(left)}."
                    f"{quote_identifier(relationship['left_column'])}"
                    f" = {quote_identifier(right)}."
                    f"{quote_identifier(relationship['right_column'])}"
                )
                joined_tables.add(right)
                added_table = True
                break

            if right in joined_tables and left not in joined_tables:
                sql += (
                    f"\nJOIN {quote_identifier(left)}"
                    f"\n  ON {quote_identifier(right)}."
                    f"{quote_identifier(relationship['right_column'])}"
                    f" = {quote_identifier(left)}."
                    f"{quote_identifier(relationship['left_column'])}"
                )
                joined_tables.add(left)
                added_table = True
                break

        if not added_table:
            return {
                "error": "Could not connect all required tables",
                "required_tables": required_tables,
            }

    conditions = []
    question_lower = question.lower()

    for column in direct_matches:
        table, column_name = column.split(".", 1)
        column_lower = column_name.lower()

        if column_lower == "injured" and "injur" in question_lower:
            conditions.append(
                f"{quote_identifier(table)}."
                f"{quote_identifier(column_name)} > 0"
            )

        elif column_lower == "killed" and "killed" in question_lower:
            conditions.append(
                f"{quote_identifier(table)}."
                f"{quote_identifier(column_name)} > 0"
            )

        elif column_lower == "country":
            match = re.search(
                r"\bin\s+([A-Z][a-zA-Z-]*)\b", question
            )
            if match:
                value = match.group(1).replace("'", "''")
                conditions.append(
                    f"{quote_identifier(table)}."
                    f"{quote_identifier(column_name)} = '{value}'"
                )

    if conditions:
        sql += "\nWHERE " + "\n  AND ".join(conditions)

    return {
        "question": question,
        "candidate_sql": sql + ";",
        "schema_links": links,
        "join_info": join_info,
    }


if __name__ == "__main__":
    question = "Show the names of people who were injured in India."

    result = generate_candidates(question, "perpetrator")
    print(json.dumps(result, indent=4))
