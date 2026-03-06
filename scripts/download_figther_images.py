import requests
from pathlib import Path
from services.roster_slots import roster_slot_service


def get_official_site_slug(slug: str) -> str:
    special_cases = {
        'hero': 'dq_hero',
        'min-min': 'minmin',
        'pyra-mythra': 'pyra',
    }

    if slug in special_cases.keys():
        return special_cases[slug]
    
    return slug.replace('-', '_')


def main():
    all_slots = roster_slot_service.get_all()
    fighter_slugs = [slot.slug.replace('-', '_') for slot in all_slots]
    failed = []

    for fighter_slug in fighter_slugs:
        output_dir = Path(f"/home/felipe/Desktop/img_api/fighters/{fighter_slug}")
        output_dir.mkdir(exist_ok=True)
        official_slug = get_official_site_slug(fighter_slug)

        for i in range(1, 9):
            n = "" if i == 1 else i
            url = f"https://www.smashbros.com/assets_v2/img/fighter/{official_slug}/main{n}.png"
            filename = output_dir / f"main{n}.png"

            response = requests.get(url)

            if response.status_code == 200:
                with open(filename, "wb") as f:
                    f.write(response.content)
                print(f"Downloaded {filename}")
            else:
                failed.append(fighter_slug)
                print(f"Failed to download {url}")

    print(f"Failed downloads: {failed}")


if __name__ == '__main__':
    main()
