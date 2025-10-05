from pydantic import BaseModel
from typing import Optional, List


class OrganizationBase(BaseModel):
    """Базовая схема организации"""
    name: str
    building_id: int


class OrganizationCreate(OrganizationBase):
    """Схема для создания организации"""
    phone_numbers: List[str] = []
    activity_ids: List[int] = []


class OrganizationUpdate(BaseModel):
    """Схема для обновления организации"""
    name: Optional[str] = None
    building_id: Optional[int] = None
    phone_numbers: Optional[List[str]] = None
    activity_ids: Optional[List[int]] = None


class PhoneBase(BaseModel):
    """Базовая схема телефона"""
    phone_number: str
    organization_id: int


class Phone(PhoneBase):
    """Схема телефона с полными данными"""
    id: Optional[int] = None

    class Config:
        from_attributes = True


class ActivitySimple(BaseModel):
    """Упрощенная схема деятельности"""
    id: int
    name: str

    class Config:
        from_attributes = True


class PhoneSimple(BaseModel):
    """Упрощенная схема телефона"""
    id: int
    phone_number: str

    class Config:
        from_attributes = True


class Organization(OrganizationBase):
    """Схема организации с полными данными"""
    id: Optional[int] = None
    activities: List[ActivitySimple] = []
    phones: List[PhoneSimple] = []

    class Config:
        from_attributes = True
