import requests
from bs4 import BeautifulSoup
import json
from slugify import slugify
from schemas.shared import SmashGames


WIKI_URL = "https://www.ssbwiki.com/Item"
OFFICIAL_SSB_SITE_URL = "https://www.smashbros.com/en_US/item/index.html"


def get_item_order():
    response = requests.get(OFFICIAL_SSB_SITE_URL)
    response.encoding = 'utf-8'
    html = response.text
    soup = BeautifulSoup(html, "html.parser")

    items = soup.find_all(None, {"class": "item-item-list__name-label"})
    ordered_names = [item.string for item in items]

    # Fix wiki/official site name mismatches
    ordered_names[ordered_names.index("Daybreak Parts")] = "Daybreak"
    ordered_names[ordered_names.index("Dragoon Parts")] = "Dragoon"
    ordered_names[ordered_names.index("Lightning")] = "Lightning Bolt"
    
    print(ordered_names)
    return ordered_names


ITEMS_ORDER = get_item_order()


def get_name(cell):
    name = cell.a.string
    return name


def get_series(cell):
    return cell.find_all('a')[-1].string


def get_notes(cell):
    return cell.get_text()


def get_heavy(cell):
    return cell.img['alt'] == "Yes"


def get_types(cell):
    return cell.string.split('/')


def get_also_appears_in(cells):
    games = [
        (SmashGames.SSB, cells[1]),
        (SmashGames.MELEE, cells[2]),
        (SmashGames.BRAWL, cells[3]),
        (SmashGames.THREE_DS, cells[4]),
        (SmashGames.WII_U, cells[4]),
    ]

    also_appears_in = []

    for game, cell in games:
        if cell.img['alt'] == "Yes":
            also_appears_in.append(game)

    return also_appears_in


def parse():
    html = requests.get(WIKI_URL).text
    soup = BeautifulSoup(html, "html.parser")

    table = soup.find("table", {"class": "wikitable sortable"})
    rows = table.find_all("tr")[1:]

    items = []

    for row in rows:
        cells = row.find_all("td")

        if not cells:
            continue

        item_not_in_ultimate = cells[5].img['alt'] == "No"

        if item_not_in_ultimate:
            continue

        name = get_name(cells[0])
        slug = slugify(name)
        series = get_series(cells[9])
        also_appears_in = get_also_appears_in(cells)
        types = get_types(cells[6])
        heavy = get_heavy(cells[7])

        item = {
            "id": ITEMS_ORDER.index(name) + 1,
            "name": name,
            "slug": slug,
            "series": series,
            "also_appears_in": also_appears_in,
            "types": types,
            "heavy": heavy,
            "notes": get_notes(cells[8]),
        }

        items.append(item)

    return items


if __name__ == "__main__":
    data = parse()
    data = sorted(data, key=lambda x: x['id'])

    with open("data/items.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print(f"Scraped {len(data)} items")