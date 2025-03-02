import pytest

from httpx import AsyncClient, ASGITransport

from second_task.main import app


@pytest.mark.parametrize("value", [10, 20, 30])
@pytest.mark.asyncio(loop_scope="session")
async def test_get_trading_dates(value):
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        response = await client.get("/api/trades/dates", params={"days": value})
        assert response.status_code == 200
        assert isinstance(response.json(), list)
        assert len(response.json()) <= value


@pytest.mark.parametrize("value", ["test_value", 1.56, None, -2, 0])
@pytest.mark.asyncio(loop_scope="session")
async def test_get_trading_dates_invalid_query_parameter(value):
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        if value is None:
            response = await client.get("/api/trades/dates")
        else:
            response = await client.get("/api/trades/dates", params={"days": value})
        assert response.status_code == 422
