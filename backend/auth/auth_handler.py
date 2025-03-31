import auth.my_security as my_security
import sqlite3
import jwt
import os
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, status, Depends
from models.user import User, UserInDB, TokenData
from datetime import datetime, timedelta, timezone
from jwt.exceptions import InvalidTokenError
from typing import Annotated
from dotenv import load_dotenv

load_dotenv() # Load environment variables from .env file

SECRET_KEY = os.environ.get("SECRET_KEY")
ALGORITHM = os.environ.get("ALGORITHM")


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_user(username: str):
    conn = sqlite3.Connection("database.db")
    conn.row_factory = lambda cursor, row: {col[0]: row[i] for i, col in enumerate(cursor.description)}
    c = conn.cursor()
    data = c.execute(f"SELECT * FROM users WHERE username = ?" , (username,))
    
    for item in data:
        if username in item.values():
            return UserInDB(**item)
        else:
            return None

def authenticate_user(username: str, password: str):
    user = get_user(username)
    if not user:
        return False
    if not my_security.verify_password(password, user.hash_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    try:
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    except Exception as e:
        raise RuntimeError(f"Token encoding failed: {str(e)}")
    return encoded_jwt

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")

        if username is None:
            raise credentials_exception
        
        token_data = TokenData(username=username)
        
    except InvalidTokenError:
        raise credentials_exception
    
    user = get_user(username=token_data.username)

    if user is None:
        raise credentials_exception
    
    return user

async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)] ):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user") 
    
    return current_user