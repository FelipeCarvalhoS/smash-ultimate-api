import json
import re
import config


def load_json(filename: str):
    path = config.DATA_DIR / filename

    with open(path, encoding='utf-8') as file:
        return json.load(file)


def get_snippet(name):
    docs_path = config.BASE_DIR / 'README.md'
    text = docs_path.read_text()
    pattern = rf"<!-- snippet:{name} -->(.*?)<!-- /snippet -->"
    match = re.search(pattern, text, re.S)
    return match.group(1).strip()
