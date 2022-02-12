import imp
from signal import raise_signal
from statistics import mode
from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import  OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, models, utils, oauth2


router = APIRouter(tags=["authentication"])

@router.post('/login', response_model=schemas.Token)

def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db:Session = Depends(get_db)):

    # USERNAME = 
    # PASSWPRD = 

    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    # CRETAE TOCKEN
    access_tocken = oauth2.create_access_tocken(data = {"user_id": user.id})

    # RETURN TOKEN

    return {"access_token": access_tocken, "token_type": "bearer"}



