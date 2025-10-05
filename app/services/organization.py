from typing import List, Optional, Set
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from app.models.organization import Organization
from app.models.building import Building
from app.models.activity import Activity
from app.models.associations import organization_activities


class OrganizationService:
    """Сервис для работы с организациями"""

    async def get_all(
        self, db: AsyncSession, skip: int = 0, limit: int = 100
    ) -> List[Organization]:
        """Получить все организации"""
        result = await db.execute(
            select(Organization)
            .options(
                selectinload(Organization.activities),
                selectinload(Organization.phones)
            )
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def get_by_id(
        self, db: AsyncSession, organization_id: int
    ) -> Organization:
        """Получить организацию по ID"""
        result = await db.execute(
            select(Organization)
            .options(
                selectinload(Organization.activities),
                selectinload(Organization.phones)
            )
            .where(Organization.id == organization_id)
        )
        return result.scalar_one_or_none()

    async def search_by_name(
        self, db: AsyncSession, name: str, skip: int = 0, limit: int = 100
    ) -> List[Organization]:
        """Поиск организаций по названию"""
        result = await db.execute(
            select(Organization)
            .options(
                selectinload(Organization.activities),
                selectinload(Organization.phones)
            )
            .where(Organization.name.ilike(f"%{name}%"))
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def get_by_activity(
        self,
        db: AsyncSession,
        activity_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[Organization]:
        """Список организаций, относящихся к указанной деятельности"""
        result = await db.execute(
            select(Organization)
            .options(
                selectinload(Organization.activities),
                selectinload(Organization.phones)
            )
            .join(
                organization_activities,
                Organization.id == organization_activities.c.organization_id,
            )
            .where(organization_activities.c.activity_id == activity_id)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def _get_activity_tree_ids(
        self, db: AsyncSession, activity_id: int
    ) -> Set[int]:
        """Получить все ID деятельностей в дереве (включая родительскую)"""
        activity_ids = {activity_id}

        result = await db.execute(
            select(Activity.id)
            .where(Activity.parent_id == activity_id)
        )
        child_ids = [row[0] for row in result.all()]

        for child_id in child_ids:
            child_tree_ids = await self._get_activity_tree_ids(db, child_id)
            activity_ids.update(child_tree_ids)

        return activity_ids

    async def get_by_activity_tree(
        self,
        db: AsyncSession,
        activity_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> List[Organization]:
        """Поиск организаций по дереву деятельности (включая дочерние)"""

        activity_ids = await self._get_activity_tree_ids(db, activity_id)

        if not activity_ids:
            return []

        result = await db.execute(
            select(Organization)
            .options(
                selectinload(Organization.activities),
                selectinload(Organization.phones)
            )
            .join(
                organization_activities,
                Organization.id == organization_activities.c.organization_id,
            )
            .where(organization_activities.c.activity_id.in_(activity_ids))
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def find_within_radius(
        self,
        db: AsyncSession,
        latitude: float,
        longitude: float,
        radius_m: float,
        activity_ids: Optional[List[int]] = None,
        search_text: Optional[str] = None,
        limit: int = 100
    ) -> List[Organization]:
        """Поиск организаций в радиусе от точки"""
        # Константа радиуса Земли в метрах
        R = 6371000

        # Формула Haversine для расчета расстояния
        lat_diff = func.radians(Building.latitude - latitude) / 2
        lon_diff = func.radians(Building.longitude - longitude) / 2
        distance_expr = (
            2 * R * func.asin(
                func.sqrt(
                    func.power(func.sin(lat_diff), 2) +
                    func.cos(func.radians(latitude)) *
                    func.cos(func.radians(Building.latitude)) *
                    func.power(func.sin(lon_diff), 2)
                )
            )
        )

        query = (
            select(Organization, distance_expr.label('distance'))
            .options(
                selectinload(Organization.activities),
                selectinload(Organization.phones)
            )
            .join(Building, Organization.building_id == Building.id)
            .where(distance_expr <= radius_m)
            .order_by('distance')
            .limit(limit)
        )

        # Фильтр по видам деятельности
        if activity_ids:
            query = query.join(
                organization_activities,
                Organization.id == organization_activities.c.organization_id
            ).where(
                organization_activities.c.activity_id.in_(activity_ids)
            )

        # Фильтр по названию
        if search_text:
            query = query.where(Organization.name.ilike(f"%{search_text}%"))

        result = await db.execute(query)
        return [row[0] for row in result.all()]

    async def find_within_rectangle(
        self,
        db: AsyncSession,
        min_latitude: float,
        max_latitude: float,
        min_longitude: float,
        max_longitude: float,
        activity_ids: Optional[List[int]] = None,
        search_text: Optional[str] = None,
        limit: int = 100
    ) -> List[Organization]:
        """Поиск организаций в прямоугольной области"""
        query = (
            select(Organization)
            .options(
                selectinload(Organization.activities),
                selectinload(Organization.phones)
            )
            .join(Building, Organization.building_id == Building.id)
            .where(
                Building.latitude.between(min_latitude, max_latitude),
                Building.longitude.between(min_longitude, max_longitude)
            )
            .limit(limit)
        )

        # Фильтр по видам деятельности
        if activity_ids:
            query = query.join(
                organization_activities,
                Organization.id == organization_activities.c.organization_id
            ).where(
                organization_activities.c.activity_id.in_(activity_ids)
            )

        # Фильтр по названию
        if search_text:
            query = query.where(Organization.name.ilike(f"%{search_text}%"))

        result = await db.execute(query)
        return result.scalars().all()

    async def create(self, db: AsyncSession, data: dict) -> Organization:
        """Создать новую организацию"""
        organization = Organization(**data)
        db.add(organization)
        await db.commit()
        await db.refresh(organization)
        return organization

    async def update(
        self, db: AsyncSession, organization_id: int, data: dict
    ) -> Organization:
        """Обновить организацию"""
        organization = await self.get_by_id(db, organization_id)
        if not organization:
            return None

        for key, value in data.items():
            setattr(organization, key, value)

        await db.commit()
        await db.refresh(organization)
        return organization

    async def delete(self, db: AsyncSession, organization_id: int) -> bool:
        """Удалить организацию"""
        organization = await self.get_by_id(db, organization_id)
        if not organization:
            return False

        await db.delete(organization)
        await db.commit()
        return True
