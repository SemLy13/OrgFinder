import logging
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.security import verify_api_key
from app.routers import health_router, organization_router, building_router

# Базовая конфигурация логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    contact={
        "name": "OrgFinder API Support",
    },
    license_info={
        "name": "MIT",
    },
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router, prefix="/api/v1", tags=["health"])
app.include_router(
    organization_router,
    prefix="/api/v1/organizations",
    tags=["organizations"],
    dependencies=[Depends(verify_api_key)]
)
app.include_router(
    building_router,
    prefix="/api/v1/buildings",
    tags=["buildings"],
    dependencies=[Depends(verify_api_key)]
)


@app.get("/")
async def root():
    return {"message": "OrgFinder API", "version": settings.VERSION}
