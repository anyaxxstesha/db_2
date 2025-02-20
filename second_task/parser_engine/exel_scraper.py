import asyncio
from asyncio import Queue
from datetime import datetime
from io import BytesIO
from typing import Any

import httpx
import pandas


def cast_int(value) -> int | None:
    try:
        return int(value)
    except ValueError:
        return None


def cast_datetime(link: str) -> datetime:
    link, *_ = link.split("?")
    return datetime.strptime(
        link, "https://spimex.com/upload/reports/oil_xls/oil_xls_%Y%m%d%H%M%S.xls"
    )


async def parse_tables(
    link_queue: Queue[str | None], data_queue: Queue[list[dict[str, Any]] | None]
):
    async def parse(link: str):
        async with httpx.AsyncClient() as client:
            response = await client.get(link)
            binary_content = await response.aread()
        dataframe = pandas.read_excel(
            BytesIO(binary_content),
            usecols="B:O",
        )
        dt = cast_datetime(link)

        res = []
        header_appeared = 0
        for row in dataframe.values:
            if (
                (deals_amount := cast_int(row[-1]))
                and deals_amount > 0
                and header_appeared == 2
            ):
                if header_appeared and (
                    row[0] == "Итого:" or row[0] == "Итого по секции:"
                ):
                    break
                res.append(
                    {
                        "exchange_product_id": row[0],
                        "exchange_product_name": row[1],
                        "oil_id": row[0][:4],
                        "delivery_basis_id": row[0][4:7],
                        "delivery_basis_name": row[2],
                        "delivery_type_id": row[0][-1],
                        "volume": cast_int(row[3]),
                        "total": cast_int(row[4]),
                        "count": deals_amount,
                        "date": dt,
                    }
                )
            if (
                row[0] == "Единица измерения: Метрическая тонна"
                or header_appeared
                and header_appeared < 2
            ):
                header_appeared += 1
        data_queue.put_nowait(res)

    page_tasks = []
    while link := await link_queue.get():
        page_tasks.append(asyncio.create_task(parse(link)))
    await asyncio.gather(*page_tasks)
    data_queue.put_nowait(None)
