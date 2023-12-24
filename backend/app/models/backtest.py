# storing backtest results
import pytz
from sqlalchemy import Column, ForeignKey, TIMESTAMP, Integer, String, BIGINT
from sqlalchemy.dialects.postgresql import JSONB
from .base import Base
from datetime import datetime


class BacktestResult(Base):
    __tablename__ = "backtest_results"

    id = Column(BIGINT, primary_key=True)
    # strategy_id = Column(BIGINT, ForeignKey("strategies.id"), nullable=False)
    strategy_name = Column(String, nullable=False)
    symbol = Column(String, nullable=False)
    t_frame = Column(String, nullable=False)
    since = Column(TIMESTAMP, nullable=False)
    type = Column(String, default="future", nullable=False)
    plot_url = Column(String)
    params = Column(JSONB)
    details = Column(JSONB)
    created_at = Column(
        TIMESTAMP(timezone=True),
        default=lambda: datetime.now(pytz.timezone("Asia/Taipei")),
        nullable=False,
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        default=lambda: datetime.now(pytz.timezone("Asia/Taipei")),
        onupdate=lambda: datetime.now(pytz.timezone("Asia/Taipei")),
    )
