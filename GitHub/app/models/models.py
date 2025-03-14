from sqlalchemy import Column, Integer, String, ForeignKey, Double, TIMESTAMP
from sqlalchemy.orm import relationship, DeclarativeBase
from sqlalchemy.sql import func



class Base(DeclarativeBase):
    pass



class Meter(Base):
    __tablename__ = "meters"

    id = Column(Integer, primary_key=True, index=True)
    meter_number = Column(String(50), unique=True, nullable=False)
    owner_name = Column(String(100), nullable=False)

    readings = relationship("Reading", back_populates="meter", cascade="all, delete")
    history = relationship("History", back_populates="meter", cascade="all, delete")



class Reading(Base):
    __tablename__ = "readings"

    id = Column(Integer, primary_key=True, index=True)
    meter_id = Column(Integer, ForeignKey("meters.id", ondelete="CASCADE"), nullable=False)
    date = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    day_kwh = Column(Double, nullable=False)
    night_kwh = Column(Double, nullable=False)

    meter = relationship("Meter", back_populates="readings")



class History(Base):
    __tablename__ = "history"

    id = Column(Integer, primary_key=True, index=True)
    meter_id = Column(Integer, ForeignKey("meters.id", ondelete="CASCADE"), nullable=False)
    date = Column(TIMESTAMP, server_default=func.now(), nullable=False)
    day_kwh = Column(Double, nullable=False)
    night_kwh = Column(Double, nullable=False)
    day_cost = Column(Double, nullable=False)
    night_cost = Column(Double, nullable=False)
    total_cost = Column(Double, nullable=False)

    meter = relationship("Meter", back_populates="history")
