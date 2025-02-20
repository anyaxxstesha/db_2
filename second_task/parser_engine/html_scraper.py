import asyncio
import httpx
from bs4 import BeautifulSoup


async def get_html(page_url):
    async with httpx.AsyncClient() as client:
        page = await client.get(page_url)
    soup = BeautifulSoup(page.text, "lxml")
    return soup


async def get_xls(queue: asyncio.Queue[str | None], page_url: str):
    next_page_url = page_url
    html_task = asyncio.create_task(get_html(next_page_url))
    while next_page_url:
        soup = await html_task
        new_tag = soup.find("li", class_="bx-pag-next").find("a")
        if new_tag is not None:
            next_page_url = f'https://spimex.com{new_tag.get("href")}'
            html_task = asyncio.create_task(get_html(next_page_url))
            await asyncio.sleep(0)
        else:
            next_page_url = None

        results = soup.find_all(
            "a", string="Бюллетень по итогам торгов в Секции «Нефтепродукты»"
        )
        for result in results:
            link = result.get("href")
            year = int(str(link).split("_")[-1][:4])
            if year > 2022:
                queue.put_nowait(f"https://spimex.com{link}")
            else:
                queue.put_nowait(None)
                return
    queue.put_nowait(None)
