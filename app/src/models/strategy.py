# This is for recording strategy name and file
from .base import Base
from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import BIGINT
# from sqlalchemy.orm import relationship

class Strategy(Base):
    __tablename__ = "strategies"
    id = Column(BIGINT, primary_key=True, index=True)
    name = Column(String, nullable=False)
    file_url = Column(String)