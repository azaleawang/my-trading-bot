import pytz
from sqlalchemy import Column, BIGINT, String, TIMESTAMP, ForeignKey
from sqlalchemy.dialects.postgresql import ARRAY, JSONB
from datetime import datetime
from .base import Base


class ContainerStatus(Base):
    __tablename__ = "container_status"

    id = Column(BIGINT, primary_key=True)
    container_id = Column(String, nullable=False)
    container_name = Column(String, nullable=False)
    status = Column(String)
    state = Column(String)
    running_for = Column(String)
    logs = Column(ARRAY(String))
    full_state = Column(JSONB)
    updated_at = Column(
        TIMESTAMP(timezone=True),
        default=lambda: datetime.now(pytz.timezone("Asia/Taipei")),
        onupdate=lambda: datetime.now(pytz.timezone("Asia/Taipei")),
    )
