import json
from pathlib import Path

project_root= Path(__file__).resolve().parent.parent
schema_path = project_root / "data" / "spider" / "tables.json"

with open(schema_path, "r", encoding ="utf-8") as f:
    schemas = json.load(f)

schema = next(
    s for s in schemas
    if s["db_id"] == "perpetrator"
)

tables = schema["table_names"]
column = schema["column_names"]

#empty list for each table

table_columns = {
    table: [] for table in tables
}

for table_index, col_n in column:
    table_name = tables[table_index]
    table_columns[table_name].append(col_n)

for table, column_list in table_columns.items():
    print(f"\nTable: {table}")
    print("Columns:", column_list)


