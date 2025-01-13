from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from second_task.config.settings import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER
from second_task.config.base import BaseModel
from second_task.domain.trading_result_model import TradingResult

_ = TradingResult

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
Session = sessionmaker(bind=engine)

def create_tables():
    BaseModel.metadata.create_all(bind=engine)
