from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.notification import Notification as NotificationModel
from app.schemas.notification import NotificationCreate, NotificationUpdate, Notification
from app.utils.error_handler import APIError, DatabaseError, logger
from typing import List
from sqlalchemy.exc import SQLAlchemyError

router = APIRouter()

@router.post("/", response_model=Notification)
async def create_notification(notification: NotificationCreate, db: Session = Depends(get_db)):
    try:
        db_notification = NotificationModel(**notification.dict())
        db.add(db_notification)
        db.commit()
        db.refresh(db_notification)
        logger.info(f"Created notification: {db_notification.id}")
        return db_notification
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error creating notification: {str(e)}")
        raise APIError(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create notification",
            error_type="database_error"
        )

@router.get("/{notification_id}", response_model=Notification)
async def read_notification(notification_id: int, db: Session = Depends(get_db)):
    try:
        db_notification = db.query(NotificationModel).filter(NotificationModel.id == notification_id).first()
        if db_notification is None:
            raise APIError(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Notification {notification_id} not found",
                error_type="not_found"
            )
        return db_notification
    except SQLAlchemyError as e:
        logger.error(f"Database error reading notification {notification_id}: {str(e)}")
        raise APIError(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve notification",
            error_type="database_error"
        )

@router.get("/", response_model=List[Notification])
async def read_notifications(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    try:
        notifications = db.query(NotificationModel).offset(skip).limit(limit).all()
        return notifications
    except SQLAlchemyError as e:
        logger.error(f"Database error reading notifications: {str(e)}")
        raise APIError(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve notifications",
            error_type="database_error"
        )

@router.put("/{notification_id}", response_model=Notification)
async def update_notification(notification_id: int, notification: NotificationUpdate, db: Session = Depends(get_db)):
    try:
        db_notification = db.query(NotificationModel).filter(NotificationModel.id == notification_id).first()
        if db_notification is None:
            raise APIError(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Notification {notification_id} not found",
                error_type="not_found"
            )
        for key, value in notification.dict().items():
            setattr(db_notification, key, value)
        db.commit()
        db.refresh(db_notification)
        logger.info(f"Updated notification: {db_notification.id}")
        return db_notification
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error updating notification {notification_id}: {str(e)}")
        raise APIError(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update notification",
            error_type="database_error"
        )

@router.delete("/{notification_id}", response_model=Notification)
async def delete_notification(notification_id: int, db: Session = Depends(get_db)):
    try:
        db_notification = db.query(NotificationModel).filter(NotificationModel.id == notification_id).first()
        if db_notification is None:
            raise APIError(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Notification {notification_id} not found",
                error_type="not_found"
            )
        db.delete(db_notification)
        db.commit()
        logger.info(f"Deleted notification: {db_notification.id}")
        return db_notification
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error deleting notification {notification_id}: {str(e)}")
        raise APIError(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete notification",
            error_type="database_error"
        )
