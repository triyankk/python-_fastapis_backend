from fastapi import APIRouter
from .endpoints import auth, users, profiles, files, health

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(profiles.router, prefix="/profiles", tags=["profiles"])
api_router.include_router(files.router, prefix="/files", tags=["files"])
api_router.include_router(health.router, prefix="/health", tags=["health"])
