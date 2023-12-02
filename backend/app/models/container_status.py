import pytz
from sqlalchemy import Column, BIGINT, String, JSON, TIMESTAMP, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from .base import Base


class ContainerStatus(Base):
    __tablename__ = "container_status"

    id = Column(BIGINT, primary_key=True)
    container_name = Column(String, ForeignKey("bots.container_name"), nullable=False)
    status = Column(String)
    state = Column(String)
    running_for = Column(String)
    logs = Column(JSON)
    full_state = Column(JSON)
    updated_at = Column(
        TIMESTAMP(timezone=True),
        default=lambda: datetime.now(pytz.timezone("Asia/Taipei")),
        onupdate=lambda: datetime.now(pytz.timezone("Asia/Taipei")),
    )
