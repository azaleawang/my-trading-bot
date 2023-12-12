from datetime import datetime
import pytz
from sqlalchemy import TIMESTAMP, Column, Integer, String, ForeignKey, BIGINT
from sqlalchemy.orm import relationship
from .base import Base

class WorkerServer(Base):
    __tablename__ = 'worker_servers'

    id = Column(BIGINT, primary_key=True)
    instance_id = Column(String, unique=True, nullable=False)
    private_ip = Column(String, unique=True)
    total_memory = Column(Integer, default=650, nullable=False)  # Total memory in MB
    available_memory = Column(Integer, default=650, nullable=False)  # Available memory in MB
    status = Column(String, default="running", nullable=False)  # running, stopped, preparing
    updated_at = Column(
        TIMESTAMP(timezone=True),
        default=lambda: datetime.now(pytz.timezone("Asia/Taipei")),
        onupdate=lambda: datetime.now(pytz.timezone("Asia/Taipei")),
    )
    bots = relationship("Bot", back_populates="worker_server")
    # TODO modify crud for separate worker server