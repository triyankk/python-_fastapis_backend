from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models.user import Base
import os
from dotenv import load_dotenv

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
