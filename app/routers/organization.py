from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from pydantic import BaseModel
from app.db.database import get_db
from app.schemas.organization import (
    Organization,
    OrganizationCreate,
    OrganizationUpdate
)
from app.services.organization import OrganizationService

router = APIRouter()
organization_service = OrganizationService()


@router.post("/", response_model=Organization)
async def create_organization(
    organization: OrganizationCreate,
    db: AsyncSession = Depends(get_db)
):
    """Создать новую организацию"""
    return await organization_service.create(db, organization.dict())


@router.get("/", response_model=List[Organization])
async def get_organizations(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    search: str = Query(None),
    db: AsyncSession = Depends(get_db)
):
    """Получить список организаций"""
    if search:
        return await organization_service.search_by_name(
            db, search, skip, limit
        )
    else:
        return await organization_service.get_all(db, skip, limit)


@router.get("/{organization_id}/", response_model=Organization)
async def get_organization(
    organization_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Получить организацию по ID"""
    organization = await organization_service.get_by_id(db, organization_id)
    if not organization:
        raise HTTPException(status_code=404, detail="Организация не найдена")
    return organization


@router.put("/{organization_id}", response_model=Organization)
async def update_organization(
    organization_id: int,
    organization: OrganizationUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Обновить организацию"""
    existing = await organization_service.get_by_id(db, organization_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Организация не найдена")

    update_data = organization.dict(exclude_unset=True)
    return await organization_service.update(db, organization_id, update_data)


@router.delete("/{organization_id}")
async def delete_organization(
    organization_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Удалить организацию"""
    existing = await organization_service.get_by_id(db, organization_id)
    if not existing:
        raise HTTPException(status_code=404, detail="Организация не найдена")

    await organization_service.delete(db, organization_id)
    return {"message": "Организация удалена"}


@router.get("/by-activity/{activity_id}/", response_model=List[Organization])
async def get_organizations_by_activity(
    activity_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_db)
):
    """Получить организации по виду деятельности"""
    return await organization_service.get_by_activity(
        db, activity_id, skip, limit
    )


@router.get(
    "/by-activity-tree/{activity_id}/",
    response_model=List[Organization]
)
async def get_organizations_by_activity_tree(
    activity_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_db)
):
    """Получить организации по дереву деятельности (включая дочерние)"""
    return await organization_service.get_by_activity_tree(
        db, activity_id, skip, limit
    )


class RadiusSearchRequest(BaseModel):
    """Схема для поиска по радиусу"""
    latitude: float
    longitude: float
    radius_m: float
    activity_ids: Optional[List[int]] = None
    search_text: Optional[str] = None
    limit: int = 100


class RectangleSearchRequest(BaseModel):
    """Схема для поиска по прямоугольнику"""
    min_latitude: float
    max_latitude: float
    min_longitude: float
    max_longitude: float
    activity_ids: Optional[List[int]] = None
    search_text: Optional[str] = None
    limit: int = 100


@router.post("/search/radius", response_model=List[Organization])
async def search_organizations_by_radius(
    request: RadiusSearchRequest,
    db: AsyncSession = Depends(get_db)
):
    """Поиск организаций в радиусе от точки"""
    return await organization_service.find_within_radius(
        db=db,
        latitude=request.latitude,
        longitude=request.longitude,
        radius_m=request.radius_m,
        activity_ids=request.activity_ids,
        search_text=request.search_text,
        limit=request.limit
    )


@router.post("/search/rectangle", response_model=List[Organization])
async def search_organizations_by_rectangle(
    request: RectangleSearchRequest,
    db: AsyncSession = Depends(get_db)
):
    """Поиск организаций в прямоугольной области"""
    return await organization_service.find_within_rectangle(
        db=db,
        min_latitude=request.min_latitude,
        max_latitude=request.max_latitude,
        min_longitude=request.min_longitude,
        max_longitude=request.max_longitude,
        activity_ids=request.activity_ids,
        search_text=request.search_text,
        limit=request.limit
    )


@router.get("/activities/tree/")
async def get_activities_tree(db: AsyncSession = Depends(get_db)):
    """Получить дерево деятельностей с уровнями вложенности"""
    from app.models.activity import Activity
    from sqlalchemy import select
    
    # Получаем все деятельности
    result = await db.execute(select(Activity))
    activities = result.scalars().all()
    
    # Группируем по уровням
    tree = {
        "level_1": [],
        "level_2": [],
        "level_3": []
    }
    
    for activity in activities:
        level_data = {
            "id": activity.id,
            "name": activity.name,
            "parent_id": activity.parent_id,
            "level": activity.level
        }
        
        if activity.level == 1:
            tree["level_1"].append(level_data)
        elif activity.level == 2:
            tree["level_2"].append(level_data)
        elif activity.level == 3:
            tree["level_3"].append(level_data)
    
    return tree
