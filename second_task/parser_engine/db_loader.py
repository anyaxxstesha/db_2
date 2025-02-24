import asyncio
from asyncio import Queue
from typing import Any

from sqlalchemy import insert
from sqlalchemy.exc import SQLAlchemyError

from second_task.config.database import Session
from second_task.domain.trading_result_model import TradingResult


async def load_chunk(chunk: list[dict[str, Any]]):
    async with Session.begin() as session:
        query = insert(TradingResult).values(chunk)
        try:
            await session.execute(query)
        except SQLAlchemyError as e:
            print("Error occured while loading chunk: ", e)


async def database_load(data_queue: Queue[list[dict[str, Any]] | None]):
    execute_tasks = []
    while chunk := await data_queue.get():
        execute_tasks.append(asyncio.create_task(load_chunk(chunk)))
    await asyncio.gather(*execute_tasks)
