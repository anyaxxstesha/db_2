import datetime
from typing import Annotated

import redis.asyncio as redis
from fastapi import Depends, HTTPException, status, Query, APIRouter
from pydantic import TypeAdapter
from sqlalchemy.ext.asyncio import AsyncSession

from second_task.config.database import get_db
from second_task.config.redis import get_redis
from second_task.services.schemas import GetTradingResult
from second_task.services.services import (
    get_last_trading_dates,
    get_dynamics,
    get_trading_results,
)

router = APIRouter(prefix="/api/trades", tags=["trades"])


@router.get("/dates")
async def get_trading_dates(
    rd: Annotated[redis.Redis, Depends(get_redis)],
    db: Annotated[AsyncSession, Depends(get_db)],
    days: Annotated[int, Query(gt=0, description="Last trading days amount")],
) -> list[datetime.datetime]:

    adapter = TypeAdapter(list[datetime.datetime])
    redis_key = f"{days}"
    cache = await rd.get(redis_key)
    if cache is not None:
        dates = adapter.validate_json(cache)
        return dates

    dates = await get_last_trading_dates(db, days)

    dates = adapter.validate_python(dates, from_attributes=True)
    json_trades = adapter.dump_json(dates).decode()
    now = datetime.datetime.now()
    if now.time() > datetime.time(14, 11):
        exp = int(
            (
                datetime.datetime(now.year, now.month, now.day + 1, 14, 11) - now
            ).total_seconds()
        )
    else:
        exp = int(
            (
                datetime.datetime(now.year, now.month, now.day, 14, 11) - now
            ).total_seconds()
        )
    await rd.set(redis_key, json_trades, ex=exp)

    if dates is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No trading dates found for the specified number of last days",
        )
    return dates


@router.get("/dynamics")
async def get_detailed_trades_info(
    rd: Annotated[redis.Redis, Depends(get_redis)],
    db: Annotated[AsyncSession, Depends(get_db)],
    start_date: Annotated[datetime.datetime, Query(description="From what date")],
    end_date: Annotated[datetime.datetime, Query(description="Till what date")],
    oil_id: Annotated[str | None, Query()] = None,
    delivery_type_id: Annotated[str | None, Query()] = None,
    delivery_basis_id: Annotated[str | None, Query()] = None,
) -> list[GetTradingResult]:

    adapter = TypeAdapter(list[GetTradingResult])
    redis_key = f"{start_date.isoformat()}-{end_date.isoformat()}-{oil_id}-{delivery_type_id}-{delivery_basis_id}"
    cache = await rd.get(redis_key)
    if cache is not None:
        trades = adapter.validate_json(cache)
        return trades

    trades = await get_dynamics(
        db, start_date, end_date, oil_id, delivery_type_id, delivery_basis_id
    )

    trades = adapter.validate_python(trades, from_attributes=True)
    json_trades = adapter.dump_json(trades).decode()
    now = datetime.datetime.now()
    if now.time() > datetime.time(14, 11):
        exp = int(
            (
                datetime.datetime(now.year, now.month, now.day + 1, 14, 11) - now
            ).total_seconds()
        )
    else:
        exp = int(
            (
                datetime.datetime(now.year, now.month, now.day, 14, 11) - now
            ).total_seconds()
        )
    await rd.set(redis_key, json_trades, ex=exp)

    if trades is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No matching trades found"
        )
    return trades


@router.get("/last")
async def get_last_trades(
    rd: Annotated[redis.Redis, Depends(get_redis)],
    db: Annotated[AsyncSession, Depends(get_db)],
    oil_id: Annotated[str | None, Query()] = None,
    delivery_type_id: Annotated[str | None, Query()] = None,
    delivery_basis_id: Annotated[str | None, Query()] = None,
) -> list[GetTradingResult]:

    adapter = TypeAdapter(list[GetTradingResult])
    redis_key = f"{oil_id}-{delivery_type_id}-{delivery_basis_id}"
    cache = await rd.get(redis_key)
    if cache is not None:
        trades = adapter.validate_json(cache)
        return trades

    trades = await get_trading_results(db, oil_id, delivery_type_id, delivery_basis_id)

    trades = adapter.validate_python(trades, from_attributes=True)
    json_trades = adapter.dump_json(trades).decode()
    now = datetime.datetime.now()
    if now.time() > datetime.time(14, 11):
        exp = int(
            (
                datetime.datetime(now.year, now.month, now.day + 1, 14, 11) - now
            ).total_seconds()
        )
    else:
        exp = int(
            (
                datetime.datetime(now.year, now.month, now.day, 14, 11) - now
            ).total_seconds()
        )
    await rd.set(redis_key, json_trades, ex=exp)

    if trades is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No last trades found for the specified details",
        )
    return trades
