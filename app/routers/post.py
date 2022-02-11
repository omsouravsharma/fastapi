from sys import prefix
from .. import models, schemas
from fastapi import Body, FastAPI,  Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List

router = APIRouter(
    prefix="/posts", 
    tags=["Posts"]
)

# GET POST

@router.get("/", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM POSTS""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts

# CREATE POSTS

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
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
    return new_post

# GET POST BY ID 

@router.get("/{id}", response_model=schemas.Post)

def get_post(id: int, response: Response, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM POSTS WHERE id = %s""", (str(id),))
    # fetched_post = cursor.fetchone()
    # print(type(id))
    fetched_post = db.query(models.Post).filter(models.Post.id == id).first()

    if not fetched_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail= f" post with id : {id} was not found")
    return fetched_post

@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
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


@router.put("/{id}", response_model=schemas.Post)
def update_post(id:int, updated_post:schemas.PostCreate,db: Session = Depends(get_db)):
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
    return post_query.first()