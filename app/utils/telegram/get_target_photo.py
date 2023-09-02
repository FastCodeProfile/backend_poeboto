import httpx
from bs4 import BeautifulSoup


async def get_target_photo(url: str):
    async with httpx.AsyncClient() as client:
        page = await client.get(url)

    soup = BeautifulSoup(page.text, "html.parser")
    img = soup.find("img", {"class": "tgme_page_photo_image"}).get("src")
    return img
