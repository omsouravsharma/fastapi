from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time
#from .config import settings

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:admin@localhost/fastapi"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
SessionLocal = Session()
Base = declarative_base()

def get_db():
    db = SessionLocal
    try: 
        yield db
    finally: 
        db.close()