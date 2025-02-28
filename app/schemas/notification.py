from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class NotificationBase(BaseModel):
    method: str
    path: str
    request_body: Optional[str] = None
    response_body: Optional[str] = None
    status_code: Optional[int] = None
    user_id: Optional[int] = None
    headers: Optional[str] = None
    client_host: Optional[str] = None
    query_params: Optional[str] = None

class NotificationCreate(NotificationBase):
    pass

class NotificationUpdate(NotificationBase):
    pass

class Notification(NotificationBase):
    id: int
    timestamp: datetime

    class Config:
        orm_mode = True
