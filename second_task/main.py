import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI

from second_task.config.database import init_models
from second_task.parser_engine.db_loader import database_load
from second_task.parser_engine.exel_scraper import parse_tables
from second_task.parser_engine.html_scraper import get_xls
from second_task.routes import router

url = "https://spimex.com/markets/oil_products/trades/results/"


async def load_data():
    link_queue = asyncio.Queue()
    data_queue = asyncio.Queue()

    await init_models()

    link_task = asyncio.create_task(get_xls(link_queue, url))
    data_task = asyncio.create_task(parse_tables(link_queue, data_queue))
    load_task = asyncio.create_task(database_load(data_queue))
    await asyncio.gather(link_task, data_task, load_task)


@asynccontextmanager
async def lifespan(app: FastAPI):
    load_data_task = asyncio.create_task(load_data())
    yield
    if not load_data_task.done():
        load_data_task.cancel()


app = FastAPI(lifespan=lifespan)
app.include_router(router)
