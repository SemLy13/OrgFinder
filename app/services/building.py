from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.models.building import Building
from app.models.organization import Organization


class BuildingService:
    """Сервис для работы со зданиями"""

    async def get_all(
        self,
        db: AsyncSession,
        skip: int = 0,
        limit: int = 100
    ) -> List[Building]:
        """Список всех зданий"""
        result = await db.execute(
            select(Building)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def get_organizations(
        self,
        db: AsyncSession,
        building_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[Organization]:
        """Список организаций в конкретном здании"""
        result = await db.execute(
            select(Organization)
            .options(
                selectinload(Organization.activities),
                selectinload(Organization.phones)
            )
            .where(Organization.building_id == building_id)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()
