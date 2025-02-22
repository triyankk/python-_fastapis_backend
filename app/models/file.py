from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base
from .enums import FileType

class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    filename = Column(String)
    file_type = Column(Enum(FileType))
    file_url = Column(String)
    mime_type = Column(String)
    size = Column(Integer)  # in bytes
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="files")
