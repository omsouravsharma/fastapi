from ast import Pass
import email
from email.mime import base
from lib2to3.pgen2.token import OP
from typing import Optional
from graphene import Int
from pydantic import BaseModel, EmailStr, conint
from datetime import datetime

from app.database import Base

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    Pass

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config: 
        orm_mode = True


class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config: 
        orm_mode = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str


    

    class Config: 
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)