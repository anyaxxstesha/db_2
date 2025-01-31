import asyncio
import time

from second_task.config.database import init_models
from second_task.parser_engine.db_loader import database_load
from second_task.parser_engine.exel_scraper import parse_tables
from second_task.parser_engine.html_scraper import get_xls

url = "https://spimex.com/markets/oil_products/trades/results/"

async def main():
    link_queue = asyncio.Queue()
    data_queue = asyncio.Queue()

    await init_models()

    link_task = asyncio.create_task(get_xls(link_queue, url))
    data_task = asyncio.create_task(parse_tables(link_queue, data_queue))
    load_task =  asyncio.create_task(database_load(data_queue))
    await asyncio.gather(link_task, data_task, load_task)


if __name__ == '__main__':
    start = time.time()
    asyncio.run(main())
    end = time.time()
    print(f"executed in {end - start}")
