import json

data = {
    "item_count": 999
}
with open("test_nested.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
