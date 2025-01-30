import asyncio

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from second_task.config.settings import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER
from second_task.config.base import BaseModel
from second_task.domain.trading_result_model import TradingResult

_ = TradingResult

DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_async_engine(DATABASE_URL, pool_pre_ping=True)
Session = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

def create_tables():
    BaseModel.metadata.create_all(bind=engine)

async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.drop_all)
        await conn.run_sync(BaseModel.metadata.create_all)

# asyncio.run(init_models())