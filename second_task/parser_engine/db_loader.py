from typing import Iterable, Any

from sqlalchemy import insert
from sqlalchemy.exc import DatabaseError

from second_task.config.database import Session
from second_task.domain.trading_result_model import TradingResult


def database_load(chunks: Iterable[list[dict[str, Any]]]):
        for chunk in chunks:
            with Session.begin() as session:
                query = insert(TradingResult).values(chunk)
                try:
                    session.execute(query)
                except DatabaseError as e:
                    print("Error occured while loading chunk: ", e)
                    session.rollback()
