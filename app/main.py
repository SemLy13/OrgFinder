from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.routers import health_router, organization_router, building_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
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
    tags=["organizations"]
)
app.include_router(
    building_router,
    prefix="/api/v1/buildings",
    tags=["buildings"]
)


@app.get("/")
async def root():
    return {"message": "OrgFinder API", "version": settings.VERSION}
