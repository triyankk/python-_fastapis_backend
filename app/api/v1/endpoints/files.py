from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from ....api import deps
from ....models import User, File as FileModel
from ....schemas import file as file_schema
from ....services.s3 import S3Service
from ....core.config import settings
from typing import List
import aiofiles
import os

router = APIRouter()
s3_service = S3Service()

@router.post("/upload", response_model=file_schema.FileInDB)
async def upload_file(
    file: UploadFile = File(...),
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    # Validate file size
    file.file.seek(0, os.SEEK_END)
    file_size = file.file.tell()
    file.file.seek(0)
    
    if file_size > settings.MAX_UPLOAD_SIZE:
        raise HTTPException(status_code=400, detail="File too large")
        
    if file.content_type not in settings.ALLOWED_FILE_TYPES:
        raise HTTPException(status_code=400, detail="File type not allowed")
    
    # Upload to S3
    file_url = await s3_service.upload_file(file)
    
    # Create file record
    db_file = FileModel(
        filename=file.filename,
        file_type="DOCUMENT" if file.content_type == "application/pdf" else "IMAGE",
        file_url=file_url,
        mime_type=file.content_type,
        size=file_size,
        user_id=current_user.id
    )
    
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    
    return db_file

@router.get("/", response_model=List[file_schema.FileInDB])
async def list_files(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    files = db.query(FileModel).filter(
        FileModel.user_id == current_user.id
    ).offset(skip).limit(limit).all()
    return files

@router.delete("/{file_id}")
async def delete_file(
    file_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user)
):
    file = db.query(FileModel).filter(
        FileModel.id == file_id,
        FileModel.user_id == current_user.id
    ).first()
    
    if not file:
        raise HTTPException(status_code=404, detail="File not found")
    
    # Delete from S3
    if await s3_service.delete_file(file.file_url):
        db.delete(file)
        db.commit()
        return {"message": "File deleted successfully"}
    
    raise HTTPException(status_code=500, detail="Error deleting file")
