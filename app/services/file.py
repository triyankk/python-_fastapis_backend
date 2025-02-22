from fastapi import UploadFile
import aiofiles
import os
from uuid import uuid4
from pathlib import Path

UPLOAD_DIR = Path("static/uploads")

async def upload_file(file: UploadFile, folder: str) -> str:
    # Create folders if they don't exist
    upload_folder = UPLOAD_DIR / folder
    upload_folder.mkdir(parents=True, exist_ok=True)
    
    # Generate unique filename
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid4()}{file_extension}"
    file_path = upload_folder / unique_filename
    
    # Save file
    async with aiofiles.open(file_path, 'wb') as out_file:
        content = await file.read()
        await out_file.write(content)
    
    # Return relative URL
    return f"/static/uploads/{folder}/{unique_filename}"
