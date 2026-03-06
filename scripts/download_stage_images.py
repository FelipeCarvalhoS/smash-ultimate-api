import requests
from pathlib import Path
from constants import TOTAL_STAGES
from services.stages import stage_service


failed = []
output_dir = Path(f"/home/felipe/Desktop/img_api/stages")
output_dir.mkdir(exist_ok=True)


def download(i):
    stage_slug = stage_service.get_by_id(i).slug

    url = f"https://www.smashbros.com/assets_v2/img/stage/stage_img{i}.jpg"
    filename = output_dir / f"{stage_slug}.png"

    response = requests.get(url)

    if response.status_code == 200:
        with open(filename, "wb") as f:
            f.write(response.content)
        print(f"Downloaded {filename}")
    else:
        failed.append(stage_slug)
        print(f"Failed to download {url}")


def download_dlc(i):
    stage_slug = stage_service.get_by_id(TOTAL_STAGES + i - 11).slug

    url = f"https://www.smashbros.com/assets_v2/img/stage/stage_addition_img{i}.jpg"
    filename = output_dir / f"{stage_slug}.png"

    response = requests.get(url)

    if response.status_code == 200:
        with open(filename, "wb") as f:
            f.write(response.content)
        print(f"Downloaded {filename}")
    else:
        failed.append(stage_slug)
        print(f"Failed to download {url}")


def main():
    for i in range(1, TOTAL_STAGES + 1 - 11):
        download(i)

    for i in range(1, 12):
        download_dlc(i)

    print(f"Failed downloads: {failed}")


if __name__ == '__main__':
    main()
