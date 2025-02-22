from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime

class ProfileBase(BaseModel):
    full_name: str
    bio: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None

class ProfileCreate(ProfileBase):
    pass

class ProfileUpdate(ProfileBase):
    full_name: Optional[str] = None

class ProfileInDB(ProfileBase):
    id: int
    user_id: int
    avatar_url: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
