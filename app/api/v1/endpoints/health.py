from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from ....api import deps
from redis import Redis
from ....core.config import settings

router = APIRouter()
redis = Redis.from_url(settings.REDIS_URL)

@router.get("/")
async def health_check(db: Session = Depends(deps.get_db)):
    health_status = {
        "status": "healthy",
        "services": {
            "api": "healthy",
            "database": "unhealthy",
            "redis": "unhealthy"
        }
    }
    
    # Check database
    try:
        db.execute(text("SELECT 1"))
        health_status["services"]["database"] = "healthy"
    except Exception:
        health_status["status"] = "unhealthy"
    
    # Check Redis
    try:
        redis.ping()
        health_status["services"]["redis"] = "healthy"
    except Exception:
        health_status["status"] = "unhealthy"
    
    return health_status
