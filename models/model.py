from sqlalchemy import Column, Integer, FLOAT, TIMESTAMP, ForeignKey
from db_handler import Base
from datetime import datetime

class Rolls(Base):
        
    __tablename__ = "rolls"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True, nullable=False)
    weight = Column(FLOAT, nullable=False)
    lenght = Column(FLOAT, nullable=False)
    added_at = Column(TIMESTAMP, default = datetime.now)
    deleted_at = Column(TIMESTAMP, nullable=True)


class Storage(Base):

    __tablename__ = "storage"
    id = Column(Integer, primary_key=True, autoincrement=True, index=True, nullable=False)
    roll_id = Column(Integer, ForeignKey("rolls.id"), nullable=False)
