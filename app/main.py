from gettext import find
from mimetypes import init
from operator import index
from turtle import pos
from typing import Optional
from fastapi import Body, FastAPI, Response, status, HTTPException, Depends
from pydantic import BaseModel
from random import randint, randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import session
from . import models
from . database import engine, get_db


models.Base.metadata.create_all(bind=engine)

app = FastAPI()



class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

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

def test_posts(db: session = Depends(get_db)):
    return {"status": "successful"}


@app.get("/posts")

def get_posts():
    cursor.execute("""SELECT * FROM POSTS""")
    posts = cursor.fetchall()
    print(posts)
    return {"data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)

def create_post(post: Post):
    cursor.execute("""INSERT INTO POSTS (title, content, published) VALUES(%s, %s, %s)
    RETURNING * """
    ,(post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}

@app.get("/posts/{id}")

def get_post(id: int, response: Response):
    cursor.execute("""SELECT * FROM POSTS WHERE id = %s""", (str(id),))
    fetched_post = cursor.fetchone()
    print(type(id))
    if not fetched_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail= f" post with id : {id} was not found")
    print(fetched_post)
    return {"post_detail": fetched_post}

@app.delete("/posts/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute(
        """DELETE FROM POSTS WHERE ID = %s RETURNING *""" , (str(id),))
    index = cursor.fetchone()
    conn.commit()
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exist.")
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id:int, post:Post):
    cursor.execute(""" UPDATE POSTS SET title = %s,
    content = %s, published = %s WHERE ID = %s RETURNING *""", (post.title,post.content,post.published,str(id)))
    index = cursor.fetchone()
    conn.commit()

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exist.")
        
    return {'message': index}

