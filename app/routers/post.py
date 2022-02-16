
from app import oauth2
from app.oauth2 import get_current_user
from .. import models, schemas
from fastapi import Body, FastAPI,  Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List, Optional
from .. import oauth2
from sqlalchemy import func

router = APIRouter(
    prefix="/posts", 
    tags=["Posts"]
)

# GET POST

@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user), limit:int = 10, skip: int =0, search:Optional[str] = ""):
    # cursor.execute("""SELECT * FROM POSTS""")
    # posts = cursor.fetchall()

    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, 
        models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    return posts

# CREATE POSTS

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO POSTS (title, content, published) VALUES(%s, %s, %s)
    # RETURNING * """
    # ,(post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    # print(post.dict())
    new_post = models.Post(owner_id = current_user.id, **post.dict())
    
    # new_post = models.Post(title=post.title, content = post.content, published = post.published)
    print(current_user.email)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

# GET POST BY ID 

@router.get("/{id}", response_model=schemas.PostOut)

def get_post(id: int, response: Response, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM POSTS WHERE id = %s""", (str(id),))
    # fetched_post = cursor.fetchone()
    # print(type(id))
    #fetched_post = db.query(models.Post).filter(models.Post.id == id).first()

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, 
        models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail= f" post with id : {id} was not found")
    return post

# DELETE POST 

@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(
    #     """DELETE FROM POSTS WHERE ID = %s RETURNING *""" , (str(id),))
    # index = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exist.")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorize to perform requested action")

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# UPDATE POST

@router.put("/{id}", response_model=schemas.Post)
def update_post(id:int, updated_post:schemas.PostCreate,db: Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute(""" UPDATE POSTS SET title = %s,
    # content = %s, published = %s WHERE ID = %s RETURNING *""", (post.title,post.content,post.published,str(id)))
    # index = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    index = post_query.first()
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} does not exist.")

    if index.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorize to perform requested action")

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()