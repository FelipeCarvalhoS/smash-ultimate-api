import json
import config


def load_json(filename: str):
    path = config.DATA_DIR / filename

    with open(path, encoding='utf-8') as file:
        return json.load(file)