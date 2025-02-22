from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"
    MODERATOR = "moderator"

class FileType(str, Enum):
    IMAGE = "image"
    DOCUMENT = "document"
    OTHER = "other"
