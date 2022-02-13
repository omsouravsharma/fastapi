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

# Database connection
# while True:

#     try: 
#         conn = psycopg2.connect(host= 'localhost', database='fastapi', user='postgres', password='admin', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("DB Connection was successful")
#         break
#     except Exception as error:
#         print("Connecting to DB failed")
#         print("Error: ".error) 
#         time.sleep(2)