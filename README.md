# DataViv Backend - Python FastAPI Service

## Overview
DataViv Backend is a Python FastAPI service that provides:
- Real-time API request tracking
- WebSocket notifications
- Database integration with PostgreSQL
- Comprehensive error handling

## Quick Start

### 1. Setup Python Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate
# Unix/MacOS
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment
Create `.env` file:
```env
DATABASE_URL=postgresql://user:password@localhost:5432/dataviv
```

### 3. Run the Application
```bash
uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```

## Project Structure
```
app/
├── models/              # SQLAlchemy models
│   ├── notification.py
│   └── user.py
├── routes/             # API routes
│   ├── notification.py
│   └── auth.py
├── services/          # Business logic
│   └── notification_service.py
├── utils/            # Utility functions
│   └── error_handler.py
└── database.py       # Database configuration
```

## Core Features

### 1. Notification System
```python
# Create notification
POST /notifications
{
    "method": "GET",
    "path": "/example",
    "status_code": 200
}

# Get notifications
GET /notifications?skip=0&limit=10
```

### 2. WebSocket Integration
```python
import websockets
import asyncio

async def connect_to_notifications():
    uri = "ws://localhost:8001/ws/notifications"
    async with websockets.connect(uri) as websocket:
        while True:
            notification = await websocket.recv()
            print(f"Received: {notification}")

# Run WebSocket client
asyncio.run(connect_to_notifications())
```

### 3. Error Handling
```python
# Using custom exceptions
try:
    result = some_operation()
except Exception as e:
    raise APIError(
        status_code=500,
        detail="Operation failed",
        error_type="operation_error"
    )

# Error response format
{
    "error": "error_type",
    "detail": "Error description",
    "status_code": 500
}
```

## API Reference

### Notifications API

```python
# Create notification
@router.post("/notifications/")
async def create_notification(...)

# Get notification by ID
@router.get("/notifications/{notification_id}")
async def read_notification(...)

# List notifications
@router.get("/notifications/")
async def read_notifications(...)

# Update notification
@router.put("/notifications/{notification_id}")
async def update_notification(...)

# Delete notification
@router.delete("/notifications/{notification_id}")
async def delete_notification(...)
```

### WebSocket API
```python
@app.websocket("/ws/notifications")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        # Handle disconnect
```

## Error Handling

### Custom Exceptions
```python
class APIError(HTTPException):
    def __init__(self, status_code: int, detail: str, error_type: str):
        super().__init__(status_code=status_code, detail=detail)
        self.error_type = error_type

class DatabaseError(Exception):
    def __init__(self, message: str, original_error: Exception = None):
        super().__init__(message)
        self.original_error = original_error
```

### Error Logging
```python
# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Log errors
try:
    # Your code
except Exception as e:
    logger.error(f"Error occurred: {str(e)}", exc_info=True)
```

## Database Operations

### Models
```python
class Notification(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True)
    method = Column(String)
    path = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
```

### Queries
```python
# Create
db.add(notification)
db.commit()

# Read
db.query(Notification).filter(Notification.id == notification_id).first()

# Update
notification.update(data)
db.commit()

# Delete
db.delete(notification)
db.commit()
```

## Development Guide

### Adding New Features
1. Create model in `app/models/`
2. Create schema in `app/schemas/`
3. Add routes in `app/routes/`
4. Include error handling
5. Add logging statements

### Testing
```bash
# Run tests
pytest

# Run specific test
pytest tests/test_notifications.py -v
```

### Debugging Tips
1. Enable debug logging
2. Use FastAPI debug mode
3. Check database logs
4. Monitor WebSocket connections

## Common Issues

### Database Connection
```python
# Check connection
from sqlalchemy import create_engine
engine = create_engine(DATABASE_URL)
try:
    connection = engine.connect()
    # Connection successful
except Exception as e:
    print(f"Connection failed: {e}")
```

### WebSocket Errors
```python
# Handle WebSocket disconnects
try:
    await websocket.send_text(message)
except WebSocketDisconnect:
    websocket_clients.remove(websocket)
except Exception as e:
    logger.error(f"WebSocket error: {e}")
```

### API Errors
```python
# Handle API errors
@app.exception_handler(APIError)
async def api_error_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.error_type, "detail": exc.detail}
    )
```
