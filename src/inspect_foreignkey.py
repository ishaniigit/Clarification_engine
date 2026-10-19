import json
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
schema_path= project_root / "data" / "spider" / "tables.json"

with open(schema_path, "r", encoding = "utf-8") as f:
    schemas = json.load(f)

schema = next(
    item for item in schemas
    if item["db_id"] == "perpetrator"
    
)

tables = schema["table_names"]
columns = schema["column_names"]
foreign_keys= schema["foreign_keys"]

print("Database:", schema["db_id"])
print("\nForeign-key relationships:")

for left_index, right_index in foreign_keys:
    left_table_index, left_column = columns[left_index]
    right_table_index, right_column = columns[right_index]

    left_table = tables[left_table_index]
    right_table = tables[right_table_index]

    print(
        f"{left_table}.{left_column} "
        f"<-> {right_table}.{right_column}"
    )
