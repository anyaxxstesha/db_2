import datetime

import pytest
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError
from starlette import status

from second_task.services.schemas import GetTradingResult
from second_task.services.services import get_dynamics


@pytest.mark.parametrize(
    "amount",
    [10, 17, 22, 89],
)
@pytest.mark.asyncio(loop_scope="session")
async def test_get_trading_results(db_session, amount):
    expected = [GetTradingResult.build() for _ in range(amount)]
    db_session.scalars.return_value.all.return_value = expected

    result = await get_dynamics(
        db_session,
        start_date=datetime.datetime.now() - datetime.timedelta(days=10),
        end_date=datetime.datetime.now(),
        oil_id="oil_id",
        delivery_type_id="delivery_type_id",
        delivery_basis_id="delivery_basis_id",
    )
    assert len(result) == amount
    assert all(isinstance(item, GetTradingResult) for item in result)


@pytest.mark.asyncio(loop_scope="session")
async def test_get_trading_results_raise_sqlalchemy_error(db_session):
    db_session.scalars.return_value.all.side_effect = SQLAlchemyError

    with pytest.raises(HTTPException) as exc:
        await get_dynamics(
            db_session,
            start_date=datetime.datetime.now() - datetime.timedelta(days=10),
            end_date=datetime.datetime.now(),
            oil_id="oil_id",
            delivery_type_id="delivery_type_id",
            delivery_basis_id="delivery_basis_id",
        )
    assert exc.value.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.asyncio(loop_scope="session")
async def test_get_trading_results_raise_404(db_session):
    db_session.scalars.return_value.all.return_value = []

    with pytest.raises(HTTPException) as exc:
        await get_dynamics(
            db_session,
            start_date=datetime.datetime.now() - datetime.timedelta(days=10),
            end_date=datetime.datetime.now(),
            oil_id="oil_id",
            delivery_type_id="delivery_type_id",
            delivery_basis_id="delivery_basis_id",
        )
    assert exc.value.status_code == status.HTTP_404_NOT_FOUND
