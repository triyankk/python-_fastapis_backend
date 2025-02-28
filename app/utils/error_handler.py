from fastapi import HTTPException, status
import logging
from typing import Dict, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class APIError(HTTPException):
    def __init__(self, status_code: int, detail: str, error_type: str = None):
        super().__init__(status_code=status_code, detail=detail)
        self.error_type = error_type
        logger.error(f"API Error: {error_type} - {detail}")

class DatabaseError(Exception):
    def __init__(self, message: str, original_error: Exception = None):
        super().__init__(message)
        self.original_error = original_error
        logger.error(f"Database Error: {message}", exc_info=original_error)

def handle_error(error: Exception) -> Dict[str, Any]:
    if isinstance(error, APIError):
        return {
            "error": error.error_type,
            "detail": error.detail,
            "status_code": error.status_code
        }
    elif isinstance(error, DatabaseError):
        return {
            "error": "database_error",
            "detail": str(error),
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR
        }
    else:
        logger.error("Unexpected error", exc_info=error)
        return {
            "error": "internal_server_error",
            "detail": "An unexpected error occurred",
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR
        }
