import json
from pathlib import Path

project_root=Path(__file__).resolve().parent.parent
schema_path=project_root / "data" / "spider" / "tables.json"

with open(schema_path,"r", encoding="utf-8") as f:
    schemas=json.load(f)

def get_schema(db_id):
    for schema in schemas:
        if schema["db_id"]==db_id:
            return schema
    return None
database_id = "perpetrator"
schema = get_schema(database_id)

if schema is not None:
    print("Database:", schema["db_id"])
    print("Tables:", schema["table_names"])

    print("\nColumns:")
    for table_index, column_name in schema["column_names"]:
        if table_index == -1:
            continue

        table_name = schema["table_names"][table_index]
        print(f"{table_name}.{column_name}")
else:
    print("Database schema not found.")

