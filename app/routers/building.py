from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.db.database import get_db
from app.schemas.building import Building
from app.schemas.organization import Organization
from app.services.building import BuildingService

router = APIRouter()
building_service = BuildingService()


@router.get("/", response_model=List[Building])
async def get_buildings(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_db)
):
    """Получить список всех зданий"""
    return await building_service.get_all(db, skip, limit)


@router.get("/{building_id}/organizations", response_model=List[Organization])
async def get_building_organizations(
    building_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_db)
):
    """Получить список организаций в конкретном здании"""
    return await building_service.get_organizations(
        db, building_id, skip, limit
    )
