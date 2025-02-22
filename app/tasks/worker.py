from celery import Celery
from ..core.config import settings
import logging

logger = logging.getLogger(__name__)

celery_app = Celery(
    "worker",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL
)

celery_app.conf.task_routes = {
    "app.tasks.worker.*": {"queue": "main-queue"}
}

@celery_app.task(acks_late=True)
def process_uploaded_file(file_id: int):
    try:
        # Add file processing logic here
        logger.info(f"Processing file {file_id}")
        return True
    except Exception as e:
        logger.error(f"Error processing file {file_id}: {e}")
        return False

@celery_app.task(acks_late=True)
def send_email_notification(user_id: int, subject: str, message: str):
    try:
        # Add email sending logic here
        logger.info(f"Sending email to user {user_id}")
        return True
    except Exception as e:
        logger.error(f"Error sending email to user {user_id}: {e}")
        return False
