from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, String, Double, Table, Text, create_engine
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, sessionmaker, mapped_column
from typing import List

Base: DeclarativeBase = declarative_base()
    
class Health(Base):
    __tablename__ = "healthLog"
    id = Column(Integer, nullable=False, autoincrement=True, primary_key=True)
    userID = Column(Integer)
    dateStamp = Column(String(50))
    height = Column(Double)
    weight = Column(Double)
    fatPercentage = Column(Double)
    musclePercentage = Column(Double)
    waterPercentage = Column(Double)
    
    
    
