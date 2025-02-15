# DataViv Backend - User Authentication API

## ✅ Requirements Checklist

### Authentication Features
- [x] User Registration
- [x] User Login
- [x] JWT Access Token
- [x] JWT Refresh Token
- [x] HTTP Cookie Storage

### API Endpoints
- [x] User Registration (/auth/register)
- [x] User Login (/auth/login)
- [x] User Details (/auth/user/me)

### Database
- [x] PostgreSQL Implementation
- [x] SQLAlchemy ORM
- [x] Persistent Data Storage

### Environment Configuration
- [x] Access Token (1 minute expiry)
- [x] Refresh Token (1 week expiry)
- [x] Environment Variables
- [x] Port 8001 Configuration

### Deployment
- [x] Docker Container
- [x] Kubernetes Setup (3 backend pods)
- [x] Database Service
- [x] Private Network
- [x] Nginx Frontend
- [x] Load Balancing (Ingress)

## 🚀 Quick Start

### Local Development Setup

1. Create and activate virtual environment:
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Unix/MacOS
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables (.env):
```env
DATABASE_URL=postgresql://user:password@host:5432/dbname
SECRET_KEY=your_secret_key
ACCESS_TOKEN_EXPIRE_MINUTES=1
REFRESH_TOKEN_EXPIRE_DAYS=7
```

4. Run the server:
```bash
# Development with reload
uvicorn main:app --reload --port 8001

# Production
python main.py
```

### 🐳 Docker Deployment

1. Build image:
```bash
docker build -t dataviv-backend:latest .
```

2. Run with Docker Compose:
```bash
docker-compose up -d
```

### ☸️ Kubernetes Deployment

1. Start Minikube:
```bash
minikube start
```

2. Configure Docker environment:
```powershell
# Windows PowerShell
& minikube -p minikube docker-env | Invoke-Expression

# Unix/Linux/MacOS
eval $(minikube docker-env)
```

3. Build image in Minikube context:
```bash
docker build -t dataviv-backend:latest .
```

4. Deploy to Kubernetes:
```bash
kubectl apply -f k8s/
```

5. Verify deployment:
```bash
kubectl get pods
kubectl get services
kubectl get ingress
```

## 🔌 API Endpoints

### Base URL: `http://localhost:8001`

1. Root Endpoint
   - URL: `/`
   - Method: `GET`
   - Response: Welcome message

2. Auth Status
   - URL: `/auth/`
   - Method: `GET`
   - Response: Server and database status

3. Register User
   - URL: `/auth/register`
   - Method: `POST`
   - Body:
     ```json
     {
       "username": "user123",
       "email": "user@example.com",
       "password": "securepass"
     }
     ```

4. User Login
   - URL: `/auth/login`
   - Method: `POST`
   - Body:
     ```json
     {
       "username": "user123",
       "password": "securepass"
     }
     ```
   - Returns: Access and refresh tokens

5. User Details
   - URL: `/auth/user/me`
   - Method: `GET`
   - Header: `Authorization: Bearer <access_token>`

## 📚 Documentation

- Swagger UI: `http://localhost:8001/docs`
- ReDoc: `http://localhost:8001/redoc`

## 🏗️ Project Structure
```
dataviv_backend/
├── app/
│   ├── models/
│   │   └── user.py
│   ├── routes/
│   │   └── auth.py
│   ├── utils/
│   │   └── auth.py
│   └── database.py
├── k8s/
│   ├── backend-deployment.yaml
│   ├── database-deployment.yaml
│   ├── ingress.yaml
│   ├── nginx-config.yaml
│   ├── nginx-deployment.yaml
│   └── postgres-pvc.yaml
├── .env
├── main.py
├── Dockerfile
└── requirements.txt
```

## 🔒 Security Features
- JWT Token Authentication
- HTTP-only Cookies
- Encrypted Password Storage
- Private Network Services
- SSL/TLS Support

## ⚙️ Configuration

### Environment Variables
- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: JWT signing key
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Access token validity (default: 1)
- `REFRESH_TOKEN_EXPIRE_DAYS`: Refresh token validity (default: 7)

### Kubernetes Services
- Backend: 3 replicas for high availability
- Database: Persistent volume with PostgreSQL
- Nginx: Load balancer and reverse proxy
- Ingress: External access management
