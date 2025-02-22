import boto3
from botocore.exceptions import ClientError
from ..core.config import settings
import logging
from fastapi import UploadFile
import uuid

logger = logging.getLogger(__name__)

class S3Service:
    def __init__(self):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY
        )
        self.bucket = settings.AWS_BUCKET_NAME

    async def upload_file(self, file: UploadFile, folder: str = "uploads") -> str:
        try:
            file_extension = file.filename.split('.')[-1]
            unique_filename = f"{folder}/{str(uuid.uuid4())}.{file_extension}"
            
            await self.s3_client.upload_fileobj(
                file.file,
                self.bucket,
                unique_filename,
                ExtraArgs={
                    "ContentType": file.content_type
                }
            )
            
            url = f"https://{self.bucket}.s3.amazonaws.com/{unique_filename}"
            return url
            
        except ClientError as e:
            logger.error(f"Error uploading file to S3: {e}")
            raise

    async def delete_file(self, file_url: str) -> bool:
        try:
            # Extract key from URL
            key = file_url.split(f"{self.bucket}.s3.amazonaws.com/")[1]
            
            await self.s3_client.delete_object(
                Bucket=self.bucket,
                Key=key
            )
            return True
            
        except ClientError as e:
            logger.error(f"Error deleting file from S3: {e}")
            return False
