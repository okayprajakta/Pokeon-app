from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# Database URL 
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:welcome1234@localhost:5432/pokemon_db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
