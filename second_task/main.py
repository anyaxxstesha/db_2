import asyncio

from second_task.config.database import create_tables, init_models
from second_task.parser_engine.db_loader import database_load
from second_task.parser_engine.exel_scraper import parse_tables

url = "https://spimex.com/markets/oil_products/trades/results/"

async def main():
    # create_tables()
    await init_models()
    gen = parse_tables(url)
    await database_load(gen)

if __name__ == '__main__':
    import timeit
    asyncio.run(main())
    # print(timeit.timeit(main, number=1))
