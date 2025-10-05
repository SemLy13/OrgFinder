import os
from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "OrgFinder"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "API для поиска организаций"

    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql+asyncpg://orgfinder_user:orgfinder_pass@"
        "localhost:5432/orgfinder"
    )

    ALLOWED_ORIGINS: List[str] = ["*"]
    API_KEY: str = os.getenv("API_KEY", "static_api_key")

    model_config = {"env_file": ".env"}


settings = Settings()
