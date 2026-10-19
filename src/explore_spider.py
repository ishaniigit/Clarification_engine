import json
from pathlib import Path

project_root= Path(__file__).resolve().parent.parent
dataset_path= project_root / "data" / "spider" / "train_spider.json"

with open(dataset_path, "r", encoding= "utf-8") as file:
    data= json.load(file)

eg= data[1]

print("Question:", eg["question"])
print("query:", eg["query"])
print("db_id:", eg["db_id"])

print(len(data))

