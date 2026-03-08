import json
import os
from config import R2_URL

def update_stages():
    filepath = "data/stages.json"
    if not os.path.exists(filepath):
        print(f"File {filepath} not found.")
        return
    
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    for item in data:
        slug = item.get("slug")
        if slug:
            # Finding where to insert "image" (under "also_appears_in")
            # We'll use a dictionary to preserve the desired order if possible, 
            # though standard json.dump handles dictionary order in Python 3.7+
            new_item = {}
            for key, value in item.items():
                new_item[key] = value
                if key == "also_appears_in":
                    new_item["image"] = f"{R2_URL}stages/{slug}.png"
            
            # Update the original list item with the ordered dictionary
            item.clear()
            item.update(new_item)
            
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"Updated {filepath}")

def update_items():
    filepath = "data/items.json"
    if not os.path.exists(filepath):
        print(f"File {filepath} not found.")
        return
    
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    for item in data:
        slug = item.get("slug")
        if slug:
            new_item = {}
            for key, value in item.items():
                new_item[key] = value
                if key == "also_appears_in":
                    new_item["image"] = f"{R2_URL}items/{slug}.png"
            
            item.clear()
            item.update(new_item)
            
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"Updated {filepath}")

def update_roster_slots():
    filepath = "data/roster_slots.json"
    if not os.path.exists(filepath):
        print(f"File {filepath} not found.")
        return
    
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    for slot_item in data:
        alts = slot_item.get("alts", [])
        for alt in alts:
            slot = alt.get("slot")
            suffix = "" if slot == 1 else slot
            alt["image"] = f"{R2_URL}roster-slots/main{suffix}.png"
            
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"Updated {filepath}")

if __name__ == "__main__":
    update_stages()
    update_items()
    update_roster_slots()
