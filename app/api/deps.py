from typing import Generator, List
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..core.security import oauth2_scheme
from ..core.config import settings
from ..models.user import User
from ..models.enums import UserRole
import jwt
from redis import Redis
from datetime import datetime, timedelta
import time

# Redis connection
redis = Redis.from_url(settings.REDIS_URL)

def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
) -> User:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        user = db.query(User).filter(User.username == payload["sub"]).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

def check_admin_access(
    current_user: User = Depends(get_current_user),
) -> User:
    if current_user.role != UserRole.ADMIN:
        raise HTTPException(
            status_code=403,
            detail="Not enough permissions"
        )
    return current_user

def rate_limit(calls: int, period: timedelta):
    async def decorator(user: User = Depends(get_current_user)):
        key = f"rate_limit:{user.id}"
        current = redis.get(key)
        
        if current is None:
            redis.setex(key, period.seconds, 1)
        elif int(current) >= calls:
            raise HTTPException(
                status_code=429,
                detail="Too many requests"
            )
        else:
            redis.incr(key)
        
        return user
    return decorator
