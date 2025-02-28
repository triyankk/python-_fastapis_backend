from sqlalchemy import text
from app.websocket import manager
from datetime import datetime
import json
from app.utils.error_handler import DatabaseError, logger

async def insert_notification(db, method: str, path: str, user_id: int = None, request_body: str = None, 
                            response_body: str = None, status_code: int = None, headers: dict = None, 
                            client_host: str = None, query_params: dict = None):
    """Logs API call details into the notifications table."""
    try:
        # Validate inputs
        if not method or not path:
            raise ValueError("Method and path are required fields")

        query = text("""
            INSERT INTO notifications (method, path, user_id, request_body, response_body, status_code, 
                                    headers, client_host, query_params, timestamp) 
            VALUES (:method, :path, :user_id, :request_body, :response_body, :status_code, 
                    :headers, :client_host, :query_params, NOW())
        """)

        # Prepare data with validation
        data = {
            "method": method,
            "path": path,
            "user_id": user_id,
            "request_body": json.dumps(request_body) if request_body else None,
            "response_body": json.dumps(response_body) if response_body else None,
            "status_code": status_code,
            "headers": json.dumps(headers) if headers else None,
            "client_host": client_host,
            "query_params": json.dumps(query_params) if query_params else None
        }

        db.execute(query, data)
        db.commit()

        logger.info(f"Notification inserted successfully: method={method}, path={path}, status_code={status_code}")

        # Prepare WebSocket notification
        notification = {
            "method": method,
            "path": path,
            "user_id": user_id,
            "request_body": request_body,
            "response_body": response_body,
            "status_code": status_code,
            "headers": headers,
            "client_host": client_host,
            "query_params": query_params,
            "timestamp": str(datetime.utcnow())
        }

        # Broadcast to all connected clients
        delivery_status = await manager.broadcast(json.dumps(notification))
        
        # Log delivery status
        logger.info(f"Notification delivery status: {delivery_status}")
        logger.info(f"Active WebSocket clients: {manager.get_status()}")
        
        return {
            "notification": notification,
            "delivery_status": delivery_status
        }

    except ValueError as ve:
        error_msg = f"Validation error: {str(ve)}"
        logger.error(error_msg)
        raise DatabaseError(error_msg, ve)

    except json.JSONDecodeError as je:
        error_msg = f"JSON encoding error: {str(je)}"
        logger.error(error_msg)
        raise DatabaseError(error_msg, je)

    except Exception as e:
        error_msg = f"Error logging API call: {str(e)}"
        logger.error(error_msg, exc_info=True)
        db.rollback()
        raise DatabaseError(error_msg, e)
