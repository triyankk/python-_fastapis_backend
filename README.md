# DataViv Backend - Python FastAPI Service

## Quick Start

### 1. Package Requirements
```bash
# Core packages
fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
passlib==1.7.4
bcrypt==4.0.1
python-jose==3.3.0
python-multipart==0.0.6
python-dotenv==1.0.0
websockets==12.0
psycopg2-binary==2.9.9
```

### 2. Installation
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

### 3. Environment Setup
```env
# .env file
DATABASE_URL=postgresql://user:password@localhost:5432/dataviv
SECRET_KEY=your_secret_key_here
```

### 4. Run Application
```bash
# Development mode
uvicorn main:app --host 0.0.0.0 --port 8001 --reload

# Production mode
uvicorn main:app --host 0.0.0.0 --port 8001
```

## Project Structure
```
dataviv_backend/
├── app/
│   ├── models/
│   │   ├── notification.py    # Notification model
│   │   └── user.py           # User model
│   ├── routes/
│   │   ├── notification.py   # Notification endpoints
│   │   └── auth.py          # Auth endpoints
│   ├── services/
│   │   └── notification_service.py  # Business logic
│   ├── utils/
│   │   └── error_handler.py  # Error handling
│   ├── websocket.py         # WebSocket manager
│   └── database.py          # DB configuration
├── main.py                  # Application entry
├── requirements.txt         # Dependencies
└── README.md               # Documentation
```

## Features

### 1. WebSocket Notifications
```python
# Connect to WebSocket
ws_url = "ws://localhost:8001/ws/notifications"

# Client example
async def connect_notifications():
    async with websockets.connect(ws_url) as websocket:
        while True:
            msg = await websocket.recv()
            print(f"Received: {msg}")
            
            # Send confirmation
            await websocket.send(json.dumps({
                "status": "received",
                "timestamp": str(datetime.utcnow())
            }))
```

### 2. Error Handling
```python
# Custom exceptions
class APIError(HTTPException):
    def __init__(self, status_code: int, detail: str, error_type: str):
        super().__init__(status_code=status_code, detail=detail)
        self.error_type = error_type

# Error response format
{
    "error": "error_type",
    "detail": "Error description",
    "status_code": 500
}
```

### 3. Notification System
```python
# Create notification
POST /notifications
{
    "method": "GET",
    "path": "/example",
    "status_code": 200
}

# List notifications
GET /notifications?skip=0&limit=10

# Get specific notification
GET /notifications/{id}
```

## Troubleshooting

### 1. Package Compatibility
If you encounter bcrypt errors:
```bash
# Uninstall existing packages
pip uninstall bcrypt passlib

# Install specific versions
pip install bcrypt==4.0.1
pip install passlib==1.7.4
```

### 2. WebSocket Connection
If WebSocket shows empty status:
```python
# Check WebSocket connection
print(f"Active clients: {manager.get_status()}")

# Monitor connection status
logger.info(f"WebSocket clients: {len(manager.active_connections)}")
```

### 3. Database Issues
```python
# Check database connection
engine = create_engine(DATABASE_URL)
try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        print("Database connected successfully")
except Exception as e:
    print(f"Database connection failed: {e}")
```

## Development Guide

### 1. Adding New Features
```python
# 1. Create model
class NewFeature(Base):
    __tablename__ = "new_features"
    id = Column(Integer, primary_key=True)
    name = Column(String)

# 2. Create schema
class NewFeatureSchema(BaseModel):
    name: str
    
    class Config:
        orm_mode = True

# 3. Add route
@router.post("/new-feature")
async def create_feature(feature: NewFeatureSchema):
    # Implementation
```

### 2. Testing WebSocket
```python
# Run test client
python test_client.py

# Monitor WebSocket connections
ws_url = "ws://localhost:8001/ws/notifications"
```

### 3. Logging
```python
# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Usage
logger.info("Operation successful")
logger.error("Operation failed", exc_info=True)
```

## API Documentation

Access the interactive API documentation at:
- Swagger UI: `http://localhost:8001/docs`
- ReDoc: `http://localhost:8001/redoc`

## Contributing

1. Fork the repository
2. Create feature branch
3. Install dependencies
4. Make changes
5. Run tests
6. Submit PR

## Common Issues

1. **bcrypt Error**: Update to bcrypt==4.0.1
2. **Empty WebSocket Status**: Check client connections
3. **Database Connection**: Verify DATABASE_URL
4. **Package Conflicts**: Use specified versions
