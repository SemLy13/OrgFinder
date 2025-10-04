from pydantic import BaseModel, Field
from typing import Optional, List


class ActivityBase(BaseModel):
    """Базовая схема деятельности"""
    name: str
    parent_id: Optional[int] = None
    level: int = Field(
        ..., ge=1, le=3, description="Уровень вложенности: 1, 2 или 3"
    )


class Activity(ActivityBase):
    """Схема деятельности с полными данными"""
    id: Optional[int] = None
    children: List["Activity"] = []
    parent: Optional["Activity"] = None

    class Config:
        from_attributes = True


# Обновляем forward references
Activity.model_rebuild()
