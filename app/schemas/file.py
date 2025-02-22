from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from ..models.enums import FileType

class FileBase(BaseModel):
    filename: str
    file_type: FileType
    mime_type: str

class FileCreate(FileBase):
    pass

class FileUpdate(BaseModel):
    filename: Optional[str] = None

class FileInDB(FileBase):
    id: int
    user_id: int
    file_url: str
    size: int
    created_at: datetime

    class Config:
        from_attributes = True
