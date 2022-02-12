from base64 import encode
from cmath import exp
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from datetime import date, datetime, timedelta
from . import schemas, database, models
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

oauth_scheme = OAuth2PasswordBearer(tokenUrl='login')

# SECRET KEY 
# Algorithm
# Expiration Time

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_tocken(data:dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def verify_access_token(token:str, credential_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        id: str = payload.get("user_id")

        if not id:
            raise credential_exception

        token_data = schemas.TokenData(id = id)
    except JWTError: 
        raise credential_exception
    return token_data


def get_current_user(token:str = Depends(oauth_scheme), db: Session = Depends(database.get_db)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                    detail=f"Could not validate credenials", 
                                    headers= {"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token, credential_exception)

    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user
