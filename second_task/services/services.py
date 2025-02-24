import datetime

from fastapi import HTTPException, status
from sqlalchemy import select, func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from second_task.domain.trading_result_model import TradingResult


async def get_last_trading_dates(
    session: AsyncSession, days_amount: int
) -> list[datetime.datetime]:
    """Returns the last trading dates as a list"""
    try:
        target_column = TradingResult.date
        trades_by_date = await session.scalars(
            select(target_column)
            .distinct(target_column)
            .order_by(target_column.desc())
            .limit(days_amount)
        )
        return list(trades_by_date.all())
    except SQLAlchemyError as e:
        print("Error occurred while implementing query: ", e)


async def get_dynamics(
    session: AsyncSession,
    start_date: datetime.datetime,
    end_date: datetime.datetime,
    oil_id: str | None = None,
    delivery_type_id: str | None = None,
    delivery_basis_id: str | None = None,
):
    """Returns a list of trades filtered by trade parameters(optional) for the specified period"""

    try:
        if end_date.hour == 0 and end_date.minute == 0 and end_date.second == 0:
            end_date = datetime.datetime(
                end_date.year, end_date.month, end_date.day, 23, 59, 59
            )
        trades = (
            select(TradingResult)
            .where(TradingResult.date > start_date, TradingResult.date < end_date)
            .order_by(TradingResult.date.desc())
        )

        if oil_id:
            trades = trades.where(TradingResult.oil_id == oil_id)
        if delivery_type_id:
            trades = trades.where(TradingResult.delivery_type_id == delivery_type_id)
        if delivery_basis_id:
            trades = trades.where(TradingResult.delivery_basis_id == delivery_basis_id)
        result = await session.scalars(trades)
        if result is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="There are no trades available",
            )
        return result.all()
    except SQLAlchemyError as e:
        print("Error occurred while implementing query: ", e)


async def get_trading_results(
    session: AsyncSession,
    oil_id: str | None = None,
    delivery_type_id: str | None = None,
    delivery_basis_id: str | None = None,
):
    """Returns a list of last trades filtered by trade parameters(optional)"""

    try:
        trades = select(TradingResult).filter(
            TradingResult.date == select(func.max(TradingResult.date)).scalar_subquery()
        )

        if oil_id:
            trades = trades.where(TradingResult.oil_id == oil_id)
        if delivery_type_id:
            trades = trades.where(TradingResult.delivery_type_id == delivery_type_id)
        if delivery_basis_id:
            trades = trades.where(TradingResult.delivery_basis_id == delivery_basis_id)
        result = await session.scalars(trades)
        if result is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="There are no trades available",
            )
        return result.all()
    except SQLAlchemyError as e:
        print("Error occurred while implementing query: ", e)


async def main_test():
    res = await get_trading_results("A100", "F")
    for r in res:
        print(r)


# asyncio.run(main_test())
