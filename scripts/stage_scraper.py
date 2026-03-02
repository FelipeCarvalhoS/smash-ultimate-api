import requests
from bs4 import BeautifulSoup
import json
from slugify import slugify
from schemas.shared import SmashGames
from schemas.stages import Availability


URL = "https://www.ssbwiki.com/Stage"


def get_id(name):
    with open("scripts/stage_order.txt", "r") as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if name in line:
                return i + 1
    exit(f"Stage '{name}' not found in stage_order.txt")


def get_availability(cell):
    availabilities = {
        '#A0F0A0': Availability.FREE_DLC,
        '#FFFFAF': Availability.PAID_DLC,
    }

    if 'style' not in cell.attrs.keys():
        return Availability.STARTER
    
    style = cell['style']
    start = style.find('#')
    end = style.find(';')
    color = style[start:end]
    return availabilities[color]


def get_name(cell):
    name = cell.a.string
    name = name if name.lower() != "pac-land" else "PAC-LAND" # Capitalize PAC-LAND to match the name used in Ultimate (the wiki uses "Pac-Land")
    return name


def get_series(cell):
    return cell.find_all('a')[1].string


def get_also_appears_in(cells):
    games = [
        (SmashGames.SSB, cells[2]),
        (SmashGames.MELEE, cells[3]),
        (SmashGames.BRAWL, cells[4]),
        (SmashGames.THREE_DS, cells[5]),
    ]

    also_appears_in = []

    if len(cells) == 7:
        games.append((SmashGames.WII_U, cells[5]))
    elif len(cells) == 8:
        games.append((SmashGames.WII_U, cells[6]))
    else:
        print(cells)
        print(f"Unexpected number of cells ({len(cells)}")
        exit(1)

    for game, cell in games:
        if cell.img['alt'] != "No":
            also_appears_in.append(game)

    return also_appears_in

def get_is_original_or_new_version(cell):
    return cell.img['alt'] != "Yes" and cell.img['alt'] != "No"


def parse():
    html = requests.get(URL).text
    soup = BeautifulSoup(html, "html.parser")

    table = soup.find("table", {"class": "wikitable sortable"})
    rows = table.find_all("tr")[1:]

    stages = []

    for row in rows:
        cells = row.find_all("td")
        if not cells:
            continue

        stage_not_in_ultimate = cells[-1].img['alt'] == "No"
        if stage_not_in_ultimate:
            continue

        name = get_name(cells[0])
        slug = slugify(name)
        id = get_id(name)
        series = get_series(cells[1])
        availability = get_availability(cells[-1])
        also_appears_in = get_also_appears_in(cells)
        is_original_or_new_version = get_is_original_or_new_version(cells[-1])

        stage = {
            "id": id,
            "name": name,
            "slug": slug,
            "series": series,
            "availability": availability,
            "also_appears_in": also_appears_in,
            "is_original_or_new_version": is_original_or_new_version,
        }

        stages.append(stage)

    return stages


if __name__ == "__main__":
    data = parse()
    data = sorted(data, key=lambda x: x['id'])

    with open("data/stages.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print(f"Scraped {len(data)} stages")