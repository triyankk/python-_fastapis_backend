from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import timedelta
import os
from ..models.user import User
from ..utils.auth import get_password_hash, verify_password, create_token, verify_token
from fastapi.security import OAuth2PasswordBearer  # Change back to OAuth2PasswordBearer
from pydantic import BaseModel
from dotenv import load_dotenv
from ..database import get_db
from ..docs.descriptions import DESCRIPTIONS

load_dotenv()
router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")  # Change back to oauth2_scheme

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str
    
@router.get("/")
async def root(db: Session = Depends(get_db)):
    try:
        # Test database connection using SQLAlchemy text()
        db.execute(text("SELECT 1"))
        return {
            "message": "server running successfully",
            "database": "connected"
        }
    except Exception as e:
        return {
            "message": "server running successfully",
            "database": "disconnected",
            "error": str(e)
        }

@router.post("/register", 
    response_model=UserResponse,
    **DESCRIPTIONS["auth_register"])
async def register(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_password = get_password_hash(user.password)
    new_user = User(username=user.username, email=user.email, hashed_password=hashed_password)
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {"message": "User created successfully"}

@router.post("/login",
    response_model=Token,
    **DESCRIPTIONS["auth_login"])
async def login(
    user: UserLogin,
    response: Response,
    db: Session = Depends(get_db)
):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_token(
        data={"sub": user.username},
        expires_delta=timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 15)))
    )
    
    refresh_token = create_token(
        data={"sub": user.username},
        expires_delta=timedelta(days=int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS")))
    )
    
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    response.set_cookie(key="refresh_token", value=refresh_token, httponly=True)
    
    return {"access_token": access_token, "refresh_token": refresh_token}

@router.get("/user/me",
    response_model=UserResponse,
    **DESCRIPTIONS["user_me"])
async def get_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    payload = verify_token(token)
    user = db.query(User).filter(User.username == payload.get("sub")).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "username": user.username,
        "email": user.email
    }
