from hashlib import new
from importlib.resources import contents
from statistics import mode
from turtle import title
from typing import Optional
from fastapi import Body, FastAPI, Query, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randint, randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models
from .database import engine, get_db
from .models import Post


models.Base.metadata.create_all(bind=engine)

app = FastAPI()



class Post(BaseModel):
    title: str
    content: str
    published: bool = True


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


@app.get("/")
def root():
    return {"message": "Welcome to my API- Sourav"}


@app.get("/sqlalchemy")

def test_posts(db: Session = Depends(get_db)):
    post = db.query(models.Post).all()
    # print(post)
    return {"data": "SS"}


@app.get("/posts")

def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM POSTS""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return {"data": posts}

# CREATE POSTS

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post, db: Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO POSTS (title, content, published) VALUES(%s, %s, %s)
    # RETURNING * """
    # ,(post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    # print(post.dict())
    new_post = models.Post(**post.dict())
    
    # new_post = models.Post(title=post.title, content = post.content, published = post.published)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}

# GET POST BY ID 

@app.get("/posts/{id}")

def get_post(id: int, response: Response, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM POSTS WHERE id = %s""", (str(id),))
    # fetched_post = cursor.fetchone()
    # print(type(id))
    fetched_post = db.query(models.Post).filter(models.Post.id == id).first()

    if not fetched_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail= f" post with id : {id} was not found")
    return {"post_detail": fetched_post}

@app.delete("/posts/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute(
    #     """DELETE FROM POSTS WHERE ID = %s RETURNING *""" , (str(id),))
    # index = cursor.fetchone()
    # conn.commit()
    index = db.query(models.Post).filter(models.Post.id == id)
    if index.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exist.")
    
    index.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id:int, updated_post:Post,db: Session = Depends(get_db)):
    # cursor.execute(""" UPDATE POSTS SET title = %s,
    # content = %s, published = %s WHERE ID = %s RETURNING *""", (post.title,post.content,post.published,str(id)))
    # index = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    index = post_query.first()
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exist.")

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return {'message': post_query.first()}

