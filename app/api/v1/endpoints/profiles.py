from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
from ....schemas import profile as profile_schema
from ....models import Profile, User
from ....api import deps
from ....services.s3 import S3Service
from ....core.config import settings

router = APIRouter()
s3_service = S3Service()

@router.post("/", response_model=profile_schema.ProfileInDB)
async def create_profile(
    profile: profile_schema.ProfileCreate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    if db.query(Profile).filter(Profile.user_id == current_user.id).first():
        raise HTTPException(status_code=400, detail="Profile already exists")
    
    db_profile = Profile(**profile.dict(), user_id=current_user.id)
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile

@router.put("/me", response_model=profile_schema.ProfileInDB)
async def update_profile(
    profile: profile_schema.ProfileUpdate,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    db_profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
    if not db_profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    for key, value in profile.dict(exclude_unset=True).items():
        setattr(db_profile, key, value)
    
    db.commit()
    db.refresh(db_profile)
    return db_profile

@router.put("/avatar")
async def update_avatar(
    file: UploadFile = File(...),
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Invalid file type")
    
    profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    avatar_url = await s3_service.upload_file(file, "avatars")
    profile.avatar_url = avatar_url
    db.commit()
    
    return {"avatar_url": avatar_url}

@router.get("/me", response_model=profile_schema.ProfileInDB)
@cached(ttl=300)  # Cache for 5 minutes
async def get_my_profile(
    current_user: User = Depends(deps.get_current_user),
    db: Session = Depends(deps.get_db)
):
    profile = db.query(Profile).filter(Profile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile
