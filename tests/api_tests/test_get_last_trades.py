import pytest
from httpx import AsyncClient, ASGITransport

from second_task.main import app


@pytest.mark.parametrize(
    "oil_id, delivery_type_id, delivery_basis_id",
    [
        ("A100", None, None),
        (None, None, None),
    ],
)
@pytest.mark.asyncio(loop_scope="session")
async def test_get_last_trades(oil_id, delivery_type_id, delivery_basis_id):
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test",
    ) as client:
        response = await client.get(
            "/api/trades/last",
            params={
                "oil_id": oil_id,
                "delivery_type_id": delivery_type_id,
                "delivery_basis_id": delivery_basis_id,
            },
        )
        assert response.status_code == 200
        assert isinstance(response.json(), list)


@pytest.mark.parametrize(
    "oil_id, delivery_type_id, delivery_basis_id",
    [
        ("test_oil7p", None, None),
        ("test_oil_0;idl", "test_delivery_id", "test_basis_id"),
    ],
)
@pytest.mark.asyncio(loop_scope="session")
async def test_get_last_trades_404(oil_id, delivery_type_id, delivery_basis_id):
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test",
    ) as client:
        response = await client.get(
            "/api/trades/last",
            params={
                "oil_id": oil_id,
                "delivery_type_id": delivery_type_id,
                "delivery_basis_id": delivery_basis_id,
            },
        )

        assert response.status_code == 404
        assert response.json().get("detail") == "There are no trades available"
