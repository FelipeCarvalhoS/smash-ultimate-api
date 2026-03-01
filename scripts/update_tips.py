import json
import re

STAR_MAP = {
    "★☆☆": "Beginner",
    "★★☆": "Intermediate",
    "★★★": "Advanced"
}

with open("data/roster_slots_tipless.json", "r", encoding="utf-8") as f:
    fighters = json.load(f)

with open("scripts/tips.txt", "r", encoding="utf-8") as f:
    tips_text = f.read()

lines = tips_text.splitlines()

current_character = None
tips_by_character = {}

star_pattern = re.compile(r"\((★{1,3}☆{0,2})\)")

for line in lines:
    line = line.strip()

    if not line:
        continue

    # Skip standalone PAL lines
    if line.startswith("PAL "):
        continue

    # Character header
    if not line.startswith("("):
        current_character = line
        tips_by_character.setdefault(current_character, [])
        continue

    star_match = star_pattern.match(line)
    if not star_match or not current_character:
        continue

    stars = star_match.group(1)

    rest = line[star_match.end():].strip()

    if " – " not in rest:
        continue

    title, content = rest.split(" – ", 1)

    # Skip PAL-exclusive tips
    if title.startswith("PAL "):
        continue

    # Remove NTSC prefix from title
    if title.startswith("NTSC "):
        title = title.replace("NTSC ", "", 1)

    # Remove NTSC prefix from content
    if content.startswith("NTSC "):
        content = content.replace("NTSC ", "", 1)

    tips_by_character[current_character].append({
        "title": title.strip(),
        "content": content.strip(),
        "level": STAR_MAP.get(stars)
    })

# Insert tips into fighters JSON
for fighter in fighters:
    name = fighter["name"]
    if name in tips_by_character:
        fighter["tips"] = tips_by_character[name]

with open("data/roster_slots_with_tips.json", "w", encoding="utf-8") as f:
    json.dump(fighters, f, indent=4, ensure_ascii=False)

print("Tips successfully added.")