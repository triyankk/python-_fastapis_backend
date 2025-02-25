from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.db.base_class import Base
import os
from dotenv import load_dotenv
import json

load_dotenv()

# Configure engine for Neon PostgreSQL
engine = create_engine(
    os.getenv("DATABASE_URL"),
    echo=True,  # Set to False in production
    pool_pre_ping=True,
    pool_recycle=60,  # Reduced for cloud DB
    pool_size=5,
    max_overflow=10,
    connect_args={
        "connect_timeout": 10,
        "sslmode": "require"  # Required for Neon
    }
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    print(f"Error creating tables: {e}")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Function to log API calls
def insert_notification(db, method: str, path: str, user_id: int = None, request_body: str = None, response_body: str = None, status_code: int = None, headers: dict = None, client_host: str = None, query_params: dict = None):
    """Logs API call details into the notifications table."""
    try:
        query = text("""
            INSERT INTO notifications (method, path, user_id, request_body, response_body, status_code, headers, client_host, query_params, timestamp) 
            VALUES (:method, :path, :user_id, :request_body, :response_body, :status_code, :headers, :client_host, :query_params, NOW())
        """)
        db.execute(query, {
            "method": method,
            "path": path,
            "user_id": user_id,
            "request_body": request_body,
            "response_body": response_body,
            "status_code": status_code,
            "headers": json.dumps(headers) if headers else None,
            "client_host": client_host,
            "query_params": json.dumps(query_params) if query_params else None
        })
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Error logging API call: {e}")
