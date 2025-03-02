import pytest
from httpx import AsyncClient, ASGITransport

from second_task.main import app


@pytest.mark.parametrize(
    "start_date, end_date, oil_id, delivery_type_id, delivery_basis_id",
    [
        ("2025-02-15", "2025-02-19", "A100", None, None),
        ("2025-02-15", "2025-02-19", None, None, None),
    ],
)
@pytest.mark.asyncio(loop_scope="session")
async def test_get_detailed_trades_info(
        start_date, end_date, oil_id, delivery_type_id, delivery_basis_id
):
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test",
    ) as client:
        response = await client.get(
            "/api/trades/dynamics",
            params={
                "start_date": start_date,
                "end_date": end_date,
                "oil_id": oil_id,
                "delivery_type_id": delivery_type_id,
                "delivery_basis_id": delivery_basis_id,
            },
        )
        assert response.status_code == 200
        assert isinstance(response.json(), list)


@pytest.mark.parametrize(
    "start_date, end_date, oil_id, delivery_type_id, delivery_basis_id",
    [
        ("2025-02-15", "2025-02-19", "oil_id2", "delivery_id", "basis_id"),
    ],
)
@pytest.mark.asyncio(loop_scope="session")
async def test_get_detailed_trades_info_404(
        start_date, end_date, oil_id, delivery_type_id, delivery_basis_id
):
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test",
    ) as client:
        response = await client.get(
            "/api/trades/dynamics",
            params={
                "start_date": start_date,
                "end_date": end_date,
                "oil_id": oil_id,
                "delivery_type_id": delivery_type_id,
                "delivery_basis_id": delivery_basis_id,
            },
        )
        print(response.json())
        assert response.status_code == 404
        assert response.json().get("detail") == "No matching trades found"


@pytest.mark.parametrize(
    "start_date, end_date, oil_id, delivery_type_id, delivery_basis_id",
    [
        ("date1", "date2", None, None, None),
    ],
)
@pytest.mark.asyncio(loop_scope="session")
async def test_get_detailed_trades_info_invalid_query_parameter(
        start_date, end_date, oil_id, delivery_type_id, delivery_basis_id
):
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test",
    ) as client:
        response = await client.get(
            "/api/trades/dynamics",
            params={
                "start_date": start_date,
                "end_date": end_date,
                "oil_id": oil_id,
                "delivery_type_id": delivery_type_id,
                "delivery_basis_id": delivery_basis_id,
            },
        )
        assert response.status_code == 422
