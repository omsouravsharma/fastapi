from ast import Pass
import email
from email.mime import base
from graphene import Int
from pydantic import BaseModel, EmailStr
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

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config: 
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str