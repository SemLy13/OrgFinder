from pydantic import BaseModel
from typing import Optional


class BuildingBase(BaseModel):
    """Базовая схема здания"""
    address: str
    latitude: float
    longitude: float


class Building(BuildingBase):
    """Схема здания с полными данными"""
    id: Optional[int] = None

    class Config:
        from_attributes = True
