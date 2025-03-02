import datetime

import pytest
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from starlette import status

from second_task.services.services import get_last_trading_dates


@pytest.mark.parametrize(
    "days_amount",
    [10, 17, 22, 26],
)
@pytest.mark.asyncio(loop_scope="session")
async def test_get_last_trading_dates(db_session, days_amount):
    db_session.scalars.return_value.all.return_value = reversed(
        [datetime.datetime(2025, 12, 1 + i) for i in range(days_amount)]
    )

    last_trading_dates = await get_last_trading_dates(db_session, days_amount)
    assert len(last_trading_dates) == days_amount


@pytest.mark.parametrize(
    "days_amount",
    [10],
)
@pytest.mark.asyncio(loop_scope="session")
async def test_get_last_trading_dates_test_raise_sqlalchemy_error(db_session, days_amount):
    db_session.scalars.return_value.all.side_effect = SQLAlchemyError
    with pytest.raises(HTTPException) as exc:
        await get_last_trading_dates(db_session, days_amount)
    assert exc.value.status_code == status.HTTP_400_BAD_REQUEST
