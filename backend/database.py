import os
import sqlite3
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

# Database Models
class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class UserProgress(Base):
    __tablename__ = "user_progress"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    challenge_id = Column(Integer, nullable=False)
    solved_at = Column(DateTime, default=datetime.utcnow)
    attempts = Column(Integer, default=1)

class UserSubmission(Base):
    __tablename__ = "user_submissions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    challenge_id = Column(Integer, nullable=False)
    query = Column(Text, nullable=False)
    passed = Column(Boolean, nullable=False)
    submitted_at = Column(DateTime, default=datetime.utcnow)

def get_database_url():
    """Get database URL based on environment"""
    database_url = os.getenv("DATABASE_URL")
    
    if database_url:
        # Production: PostgreSQL (future)
        return database_url
    else:
        # Development: SQLite
        db_path = os.getenv("DATABASE_PATH", "users.db")
        return f"sqlite:///{db_path}"

def get_engine():
    """Get SQLAlchemy engine"""
    database_url = get_database_url()
    
    if database_url.startswith("sqlite"):
        # SQLite for development
        return create_engine(database_url, connect_args={"check_same_thread": False})
    else:
        # PostgreSQL for production (future)
        return create_engine(database_url)

def get_session():
    """Get database session"""
    engine = get_engine()
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return SessionLocal()

def init_database():
    """Initialize database tables"""
    engine = get_engine()
    Base.metadata.create_all(bind=engine)

# Legacy SQLite functions for backward compatibility
def get_sqlite_connection():
    """Get SQLite connection for legacy code"""
    db_path = os.getenv("DATABASE_PATH", "users.db")
    return sqlite3.connect(db_path) 