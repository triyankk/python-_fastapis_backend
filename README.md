# 🚀 DataViv Backend - Complete FastAPI Reference

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Quick Start](#quick-start)
- [Detailed Setup](#detailed-setup)
- [API Documentation](#api-documentation)
- [Development Guide](#development-guide)
- [Deployment Options](#deployment-options)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)

## Introduction

A production-ready FastAPI backend template with authentication, database integration, and cloud deployment support.

### Tech Stack
- **FastAPI**: Modern web framework
- **PostgreSQL**: Primary database
- **Redis**: Caching and rate limiting
- **SQLAlchemy**: ORM
- **Alembic**: Database migrations
- **JWT**: Authentication
- **Docker**: Containerization
- **Kubernetes**: Orchestration

## Features

### 🔐 Authentication & Security
- JWT token authentication
- Refresh token mechanism
- Password hashing with bcrypt
- Rate limiting
- HTTP-only cookies
- Role-based access control (Admin/User/Moderator)
- Email verification

### 💾 Data Management
- PostgreSQL integration
- Redis caching
- File uploads to S3
- Background tasks
- Database migrations

### 🔍 Monitoring & Logging
- Prometheus metrics
- Health checks
- Request logging
- Error tracking

### 🚀 DevOps Ready
- Docker support
- Kubernetes configurations
- Nginx reverse proxy
- Load balancing
- SSL/TLS support

## Quick Start

### 1. Clone and Setup
```bash
# Clone repository
git clone <repository-url>
cd dataviv_backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment
Create `.env` file:
```env
# Required Settings
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
SECRET_KEY=your-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=1
REFRESH_TOKEN_EXPIRE_DAYS=7

# Optional Features
REDIS_URL=redis://localhost:6379
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_BUCKET_NAME=your_bucket

# Email Settings
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your@email.com
SMTP_PASSWORD=app_password
```

### 3. Run Application
```bash
# Development
uvicorn main:app --reload --port 8001

# Production
uvicorn main:app --host 0.0.0.0 --port 8001
```

## API Documentation

### Authentication Endpoints

#### Register User
```bash
POST /api/v1/auth/register
{
    "username": "user123",
    "email": "user@example.com",
    "password": "securepass123"
}
```

#### Login
```bash
POST /api/v1/auth/login
{
    "username": "user123",
    "password": "securepass123"
}
```

#### Profile Management
```bash
# Get profile
GET /api/v1/profiles/me

# Update profile
PUT /api/v1/profiles/me
{
    "full_name": "John Doe",
    "bio": "Software Developer"
}

# Upload avatar
POST /api/v1/profiles/avatar
Content-Type: multipart/form-data
```

## Development Guide

### Project Structure
```
dataviv_backend/
├── app/
│   ├── api/
│   │   ├── v1/
│   │   │   ├── endpoints/     # API routes
│   │   │   └── api.py        # Router registration
│   │   └── deps.py          # Dependencies
│   ├── core/
│   │   ├── config.py        # Settings
│   │   └── security.py      # Security utils
│   ├── models/              # Database models
│   ├── schemas/             # Pydantic schemas
│   ├── services/            # Business logic
│   └── tests/               # Test files
├── migrations/              # Alembic migrations
└── k8s/                    # Kubernetes configs
```

### Database Migrations
```bash
# Create migration
alembic revision --autogenerate -m "description"

# Apply migration
alembic upgrade head

# Rollback
alembic downgrade -1
```

### Running Tests
```bash
# All tests
pytest

# With coverage
pytest --cov=app --cov-report=html

# Single test file
pytest app/tests/test_auth.py -v
```

## Deployment Options

### Docker Deployment
```bash
# Build and run
docker-compose up --build

# Production mode
docker-compose -f docker-compose.prod.yml up -d
```

### Kubernetes Deployment
```bash
# Start Minikube
minikube start

# Deploy application
kubectl apply -f k8s/

# Verify deployment
kubectl get pods
kubectl get services
```

## Advanced Features

### Redis Caching
```python
from app.cache.redis_cache import cached

@router.get("/items")
@cached(ttl=300)  # Cache for 5 minutes
async def get_items():
    return items
```

### Background Tasks
```python
from app.tasks.worker import process_uploaded_file

@router.post("/upload")
async def upload(background_tasks: BackgroundTasks):
    background_tasks.add_task(process_uploaded_file)
```

### Custom Middleware
```python
from app.middleware.logging import logging_middleware
app.middleware("http")(logging_middleware)
```

## Troubleshooting

### Common Issues

1. Database Connection
```bash
# Verify PostgreSQL
psql -h localhost -U postgres -d auth_db

# Check migrations
alembic current
alembic history
```

2. Authentication Issues
```bash
# Clear tokens
redis-cli
> FLUSHALL

# Check JWT
python -c "import jwt; print(jwt.decode(token, verify=False))"
```

3. Kubernetes Issues
```bash
# Check pods
kubectl describe pod <pod-name>

# View logs
kubectl logs <pod-name>

# Port forward
kubectl port-forward service/backend 8001:8001
```

## Security Best Practices

1. Environment Variables
- Never commit .env files
- Use strong SECRET_KEY
- Rotate credentials regularly

2. API Security
- Rate limiting enabled
- CORS properly configured
- Input validation with Pydantic
- SQL injection prevention

3. Password Security
- Bcrypt hashing
- Password strength validation
- Secure token storage

## Contributing

1. Fork the repository
2. Create feature branch
3. Commit changes
4. Create pull request

## Support

Need help? Check out:
- [Documentation](https://fastapi.tiangolo.com/)
- [Issue Tracker](https://github.com/your-repo/issues)
- [Discord Community](https://discord.gg/your-channel)
