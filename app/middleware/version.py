from fastapi import Request
from typing import Callable
from ..core.config import settings

async def version_middleware(request: Request, call_next: Callable):
    response = await call_next(request)
    response.headers["X-API-Version"] = settings.VERSION
    return response
