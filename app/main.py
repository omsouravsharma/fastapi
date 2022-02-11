from pyexpat import model
from typing import List
from hashlib import new
from importlib.resources import contents
from statistics import mode
from typing import Optional
from fastapi import Body, FastAPI, Query, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randint, randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import engine, get_db
from .routers import post, user, auth


models.Base.metadata.create_all(bind=engine)

app = FastAPI()





# Database connection

while True:

    try: 
        conn = psycopg2.connect(host= 'localhost', database='fastapi', user='postgres', password='admin', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("DB Connection was successful")
        break
    except Exception as error:
        print("Connecting to DB failed")
        print("Error: ".error) 
        time.sleep(2)

my_posts = [{"title": "title of post", "content":"content of post", "id": 1}, 
            {"title": "favourite food", "content":"I like pizza", "id": 2}]


def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p["id"] ==id:
            return i

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "Welcome to my API- Sourav"}