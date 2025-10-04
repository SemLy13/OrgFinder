from pydantic import BaseModel, EmailStr
from typing import Optional, List


class OrganizationBase(BaseModel):
    """Базовая схема организации"""
    name: str
    description: Optional[str] = None
    email: Optional[EmailStr] = None
    website: Optional[str] = None
    building_id: int


class OrganizationCreate(OrganizationBase):
    """Схема для создания организации"""
    phone_numbers: List[str] = []
    activity_ids: List[int] = []


class OrganizationUpdate(BaseModel):
    """Схема для обновления организации"""
    name: Optional[str] = None
    description: Optional[str] = None
    email: Optional[EmailStr] = None
    website: Optional[str] = None
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


class Organization(OrganizationBase):
    """Схема организации с полными данными"""
    id: Optional[int] = None
    building: Optional["Building"] = None
    activities: List["Activity"] = []
    phones: List["Phone"] = []

    class Config:
        from_attributes = True


# Импорты для forward references
from app.schemas.building import Building  # noqa
from app.schemas.activity import Activity  # noqa

# Обновляем forward references
Organization.model_rebuild()
