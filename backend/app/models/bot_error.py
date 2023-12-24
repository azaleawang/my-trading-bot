import datetime
import pytz
from sqlalchemy import Column, ForeignKey, Integer, String, TIMESTAMP
from .base import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class BotError(Base):
    __tablename__ = 'bot_error'

    id = Column(Integer, primary_key=True, index=True)
    container_name = Column(String, ForeignKey("bots.container_name"), nullable=False)
    error = Column(String, nullable=False)
    timestamp = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    
    bot = relationship("Bot", back_populates="error")