from datetime import datetime
from io import BytesIO

import requests

from second_task.parser_engine.html_scraper import get_xls
import pandas


def cast_int(value) -> int | None:
    try:
        return int(value)
    except ValueError:
        return None

def cast_datetime(link: str) -> datetime:
    link, *_ = link.split('?')
    return datetime.strptime(link, "https://spimex.com/upload/reports/oil_xls/oil_xls_%Y%m%d%H%M%S.xls")


def parse_tables(url):
    for link in get_xls(url):
        page = requests.get(link)
        binary_content = page.content
        dataframe = pandas.read_excel(BytesIO(binary_content), usecols="B:O", skiprows=8, skipfooter=2)
        dt = cast_datetime(link)

        yield [
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
            for row in dataframe.values
            if (deals_amount := cast_int(row[-1])) and deals_amount > 0
        ]
