from sqlalchemy import Column, Integer, String, DateTime, Text
from app.db.base_class import Base
from datetime import datetime

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    method = Column(String(10))
    path = Column(String(255))
    request_body = Column(Text, nullable=True)
    response_body = Column(Text, nullable=True)
    status_code = Column(Integer, nullable=True)
    user_id = Column(Integer, nullable=True)
    headers = Column(Text, nullable=True)
    client_host = Column(String(255), nullable=True)
    query_params = Column(Text, nullable=True)
