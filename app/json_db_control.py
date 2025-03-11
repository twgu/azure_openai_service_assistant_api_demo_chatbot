import json


def load_json(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read().strip()
            return json.loads(content) if content else {}
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_json(filepath, data):
    with open(filepath, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
