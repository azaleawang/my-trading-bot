from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from .base import Base
from sqlalchemy.dialects.postgresql import BIGINT

class User(Base):
    __tablename__ = "users"

    id = Column(BIGINT, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    bots = relationship("Bot", back_populates="owner")
    strategies = relationship("Strategy", back_populates="provider")