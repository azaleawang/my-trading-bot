import pytz
from sqlalchemy import Column, ForeignKey, String, Text
from sqlalchemy.orm import relationship
from .base import Base
from sqlalchemy.dialects.postgresql import BIGINT, TIMESTAMP, ENUM
from datetime import datetime

# create bot model
class Bot(Base):
    __tablename__ = "bots"

    id = Column(BIGINT, primary_key=True, index=True)
    container_id = Column(String)
    container_name = Column(String)
    name = Column(String, nullable=False)
    strategy = Column(String, default="supertrend")
    description = Column(Text)
    created_at = Column(TIMESTAMP(timezone=True), default=lambda: datetime.now(pytz.timezone('Asia/Taipei')), nullable=False)
    status = Column(
        ENUM("running", "stopped", "deleted", name="status_type"),
        default="running",
        nullable=False,
    )
    owner_id = Column(BIGINT, ForeignKey("users.id"))
    owner = relationship("User", back_populates="bots")