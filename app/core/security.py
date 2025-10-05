from fastapi import HTTPException, Header
from app.core.config import settings


async def verify_api_key(authorization: str = Header(...)):
    """Проверка API ключа из заголовка Authorization"""
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Неверный формат авторизации. Используйте: Bearer {api_key}"
        )

    api_key = authorization[7:]  # Убираем "Bearer "

    if not api_key or api_key != settings.API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Неверный API ключ"
        )

    return api_key
