from fastapi import APIRouter, Depends, HTTPException, Response, BackgroundTasks
from sqlalchemy.orm import Session
from ....core.config import settings
from ....core import security
from ....schemas import user as user_schema
from ....models import user as user_model
from ....api import deps
from ....services import email as email_service
from fastapi.security import OAuth2PasswordBearer
from datetime import timedelta

router = APIRouter()

@router.post("/register", response_model=user_schema.UserResponse)
async def register(
    user: user_schema.UserCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(deps.get_db)
):
    # Check existing user
    if db.query(user_model.User).filter(user_model.User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create user
    db_user = user_model.User(
        email=user.email,
        username=user.username,
        hashed_password=security.get_password_hash(user.password),
        is_active=False
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # Send verification email
    verification_token = security.create_email_verification_token(db_user)
    background_tasks.add_task(
        email_service.send_verification_email,
        email_to=user.email,
        token=verification_token
    )
    
    return db_user

# ...existing login endpoint with rate limiting...
@router.post("/login", response_model=user_schema.Token)
@deps.rate_limit(calls=5, period=timedelta(minutes=5))
async def login(
    response: Response,
    credentials: user_schema.UserLogin,
    db: Session = Depends(deps.get_db)
):
    # ...existing login code...

# New endpoint for email verification
@router.get("/verify-email/{token}")
async def verify_email(token: str, db: Session = Depends(deps.get_db)):
    email = security.verify_email_token(token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid verification token")
    
    user = db.query(user_model.User).filter(user_model.User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.is_active = True
    db.commit()
    return {"message": "Email verified successfully"}

# Password reset endpoints
@router.post("/forgot-password")
async def forgot_password(
    email: user_schema.EmailSchema,
    background_tasks: BackgroundTasks,
    db: Session = Depends(deps.get_db)
):
    user = db.query(user_model.User).filter(user_model.User.email == email.email).first()
    if user:
        reset_token = security.create_password_reset_token(user)
        background_tasks.add_task(
            email_service.send_password_reset_email,
            email_to=email.email,
            token=reset_token
        )
    return {"message": "If your email is registered, you will receive a password reset link"}

@router.post("/reset-password/{token}")
async def reset_password(
    token: str,
    new_password: user_schema.PasswordReset,
    db: Session = Depends(deps.get_db)
):
    email = security.verify_password_reset_token(token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid reset token")
    
    user = db.query(user_model.User).filter(user_model.User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.hashed_password = security.get_password_hash(new_password.new_password)
    db.commit()
    return {"message": "Password updated successfully"}
