import json
from pathlib import Path

project_root= Path(__file__).resolve().parent.parent
dataset_path= project_root/ "data" / "spider" / "train_spider.json"

with open(dataset_path, "r", encoding="utf-8") as file:
          data= json.load(file)

print("total training examples:", len(data))

print("first training eg:")
print(json.dumps(data[0], indent=4, ensure_ascii=False))