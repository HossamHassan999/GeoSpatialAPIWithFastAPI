from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

from dotenv import load_dotenv

load_dotenv()

ATABASE_URL = os.getenv("DATABASE_URL")   

engine = create_engine(ATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()