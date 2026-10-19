import json
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
schema_path= project_root / "data" / "spider" / "tables.json"

with open(schema_path, "r", encoding = "utf-8") as f:
    schemas= json.load(f)

print("total dbs:", len(schemas))

schema= schemas[0]

print("\ndb_id:", schema["db_id"])
print("\ntable_names:", schema["table_names"])
print("\nColumn names:")

for col in schema["column_names"]:
    print(col)

