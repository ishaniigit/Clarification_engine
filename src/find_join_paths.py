
import json
from pathlib import Path
from collections import deque

project_root = Path(__file__).resolve().parent.parent
schema_path = project_root / "data" / "spider" / "tables.json"

with open(schema_path, "r", encoding="utf-8") as f:
    schemas = json.load(f)


def find_join_paths(schema, matched_tables):
    tables = schema["table_names"]
    columns = schema["column_names"]

    graph = {table: [] for table in tables}

    for left_index, right_index in schema["foreign_keys"]:
        left_table_index, left_column = columns[left_index]
        right_table_index, right_column = columns[right_index]

        left_table = tables[left_table_index]
        right_table = tables[right_table_index]

        edge = {
            "left_table": left_table,
            "left_column": left_column,
            "right_table": right_table,
            "right_column": right_column,
        }

        graph[left_table].append((right_table, edge))
        graph[right_table].append((
            left_table,
            {
                "left_table": right_table,
                "left_column": right_column,
                "right_table": left_table,
                "right_column": left_column,
            }
        ))

    required_tables = set(matched_tables)
    join_relationships = {}

    for i in range(len(matched_tables)):
        for j in range(i + 1, len(matched_tables)):
            start = matched_tables[i]
            target = matched_tables[j]

            queue = deque([(start, [])])
            visited = {start}
            found_path = None

            while queue:
                current, path = queue.popleft()

                if current == target:
                    found_path = path
                    break

                for neighbor, edge in graph[current]:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        queue.append((neighbor, path + [edge]))

            if found_path is not None:
                for edge in found_path:
                    required_tables.add(edge["left_table"])
                    required_tables.add(edge["right_table"])

                    key = (
                        edge["left_table"],
                        edge["left_column"],
                        edge["right_table"],
                        edge["right_column"],
                    )
                    join_relationships[key] = edge

    return {
        "matched_tables": matched_tables,
        "required_tables": sorted(required_tables),
        "join_relationships": list(join_relationships.values()),
    }


def get_schema(db_id):
    for schema in schemas:
        if schema["db_id"] == db_id:
            return schema
    return None

if __name__ == "__main__":  

    schema = get_schema("perpetrator")

    if schema is None:
        print("Database not found.")
    else:
        result = find_join_paths(
            schema,
            ["perpetrator", "people"]
        )
        print(json.dumps(result, indent=4))
