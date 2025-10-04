from sqlalchemy import Column, Integer, Float, Text
from app.models import Base


class Building(Base):
    """Здания"""
    __tablename__ = "buildings"

    id = Column(Integer, primary_key=True, index=True)
    address = Column(Text, nullable=False)
    latitude = Column(Float, nullable=False)  # Широта
    longitude = Column(Float, nullable=False)  # Долгота
