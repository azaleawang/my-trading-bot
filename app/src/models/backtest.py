# storing backtest results
import pytz
from sqlalchemy import Column, ForeignKey, TIMESTAMP, Integer, String, BIGINT
from sqlalchemy.dialects.postgresql import JSONB
from .base import Base
from datetime import datetime
from sqlalchemy.sql import func


class Backtest_Result(Base):
    __tablename__ = "backtest_results"
    
    id = Column(BIGINT, primary_key=True)
    strategy_id = Column(BIGINT, ForeignKey("strategies.id"), nullable=False)
    symbol = Column(String, nullable=False)
    since = Column(TIMESTAMP, nullable=False)
    type = Column(String, default="future", nullable=False)
    s3_url = Column(String)
    params = Column(JSONB)
    created_at = Column(TIMESTAMP(timezone=True), default=lambda: datetime.now(pytz.timezone('Asia/Taipei')), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), onupdate=lambda: datetime.now(pytz.timezone('Asia/Taipei')))