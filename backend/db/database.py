from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from core.config import Settings

settings = Settings()

# Create engine using the database URL from settings
engine = create_engine(
    settings.DATABASE_URL
)

# Configure session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for declarative models
Base = declarative_base()

# Dependency for getting a session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Function to create tables
def create_tables():
    Base.metadata.create_all(engine)