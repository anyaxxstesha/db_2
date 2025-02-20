from datetime import datetime

from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

from second_task.config.base import BaseModel


class TradingResult(BaseModel):
    __tablename__ = "spimex_trading_results"

    id: Mapped[int] = mapped_column(primary_key=True)
    exchange_product_id: Mapped[str] = mapped_column()
    exchange_product_name: Mapped[str] = mapped_column()
    oil_id: Mapped[str] = mapped_column()
    delivery_basis_id: Mapped[str] = mapped_column()
    delivery_basis_name: Mapped[str] = mapped_column()
    delivery_type_id: Mapped[str] = mapped_column()
    volume: Mapped[int] = mapped_column(nullable=True)
    total: Mapped[int] = mapped_column(nullable=True)
    count: Mapped[int] = mapped_column(nullable=True)
    date: Mapped[datetime] = mapped_column()
    created_on: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_on: Mapped[datetime] = mapped_column(
        server_onupdate=func.now(), server_default=func.now()
    )

    def __repr__(self) -> str:
        return (
            f"TradingResult(id={self.id!r}, exchange_product_id={self.exchange_product_id!r},"
            f" exchange_product_name={self.exchange_product_name!r}, oil_id={self.oil_id!r},"
            f" delivery_basis_id={self.delivery_basis_id!r}, delivery_basis_name={self.delivery_basis_name!r},"
            f" delivery_type_id={self.delivery_type_id!r}, volume={self.volume!r}, total={self.total!r},"
            f" count={self.count!r}, date={self.date!r}, created_on={self.created_on!r}, updated_on={self.updated_on!r}"
        )
