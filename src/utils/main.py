#src/utils/main.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.config.database import SQLALCHEMY_DATABASE_URL  # Make sure you define the DATABASE_URL in your config

# Create the database engine and session
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()