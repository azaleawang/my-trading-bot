# This is for recording strategy name and file
from .base import Base
from sqlalchemy import Column, ForeignKey, String, Boolean
from sqlalchemy.dialects.postgresql import BIGINT
from sqlalchemy.orm import relationship


class Strategy(Base):
    __tablename__ = "strategies"
    id = Column(BIGINT, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    file_url = Column(String)
    provider_id = Column(BIGINT, ForeignKey("users.id"))
    provider = relationship("User", back_populates="strategies")
    is_public = Column(Boolean, server_default="true", nullable=False)
