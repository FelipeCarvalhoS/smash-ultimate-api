from bs4 import BeautifulSoup
import requests
from pathlib import Path
from constants import ITEMS_TOTAL
from services.items import item_service


ITEM_PAGE_URL = 'https://www.smashbros.com/en_US/item/index.html'
failed = []
output_dir = Path(f"/home/felipe/Desktop/img_api/items")
output_dir.mkdir(exist_ok=True)


def get_image_spans():
    html = requests.get(ITEM_PAGE_URL).text
    soup = BeautifulSoup(html, "html.parser")
    spans = soup.find_all("span", {"class": "item-item-list__img-thumb"})
    return spans

IMAGE_SPANS = get_image_spans()



def main():
    for i, span in enumerate(IMAGE_SPANS):
        img_url = span['style'][21:].rstrip(');')
        full_url = 'https://www.smashbros.com' + img_url

        item_slug = item_service.get_by_id(i+1).slug
        filename = output_dir / f"{item_slug}.png"

        response = requests.get(full_url)

        if response.status_code == 200:
            with open(filename, "wb") as f:
                f.write(response.content)
            print(f"Downloaded {filename}")
        else:
            failed.append(item_slug)
            print(f"Failed to download {full_url}")


if __name__ == '__main__':
    main()
