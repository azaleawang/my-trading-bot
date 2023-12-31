import pytz
from sqlalchemy import Column, ForeignKey, String, Text, Float, Integer
from sqlalchemy.orm import relationship
from .base import Base
from sqlalchemy.dialects.postgresql import BIGINT, TIMESTAMP
from datetime import datetime


# create bot model
class Bot(Base):
    __tablename__ = "bots"

    id = Column(BIGINT, primary_key=True, index=True)
    container_id = Column(String, unique=True, nullable=False)
    container_name = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    strategy = Column(String, default="supertrend")
    symbol = Column(String, default="ETH/USDT", nullable=False)
    t_frame = Column(String, default="1d")
    quantity = Column(Float, default=0.1, nullable=False)
    description = Column(Text)
    created_at = Column(
        TIMESTAMP(timezone=True),
        default=lambda: datetime.now(pytz.timezone("Asia/Taipei")),
        nullable=False,
    )
    stopped_at = Column(TIMESTAMP(timezone=True))
    status = Column(
        String,
        default="running",
        nullable=False,
    )
    owner_id = Column(BIGINT, ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="bots")
    trade_history = relationship(
        "TradeHistory", back_populates="bot", cascade="all, delete-orphan"
    )
    error = relationship(
        "BotError", back_populates="bot", cascade="all, delete-orphan"
    )
    container_status = relationship(
        "ContainerStatus", back_populates="bot", cascade="all, delete-orphan"
    )
    memory_usage = Column(Integer, default=128)  # Memory usage in MB
    worker_instance_id = Column(String, ForeignKey('worker_servers.instance_id'))
    worker_server = relationship("WorkerServer", back_populates="bots")
