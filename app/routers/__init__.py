from .health import router as health_router
from .organization import router as organization_router
from .building import router as building_router

__all__ = [
    "health_router",
    "organization_router",
    "building_router"
]
