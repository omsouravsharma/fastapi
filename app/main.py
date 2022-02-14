from distutils.command.config import config
from telnetlib import SE
from fastapi import  FastAPI
from . import models, config
from .database import engine
from .routers import post, user, auth, vote


from app import database




models.Base.metadata.create_all(bind=engine)

app = FastAPI()


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
app.include_router(vote.router)

@app.get("/")
def root():
    return {"message": "Welcome to my API- Sourav"}