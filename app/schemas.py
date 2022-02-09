from ast import Pass
from email.mime import base
from pydantic import BaseModel
from datetime import datetime

from app.database import Base

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    Pass

class Post(PostBase):
    id: int
    created_at: datetime

    class Config: 
        orm_mode = True