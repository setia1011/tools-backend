import time
from typing import List
from fastapi.logger import logger
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from passlib.context import CryptContext
from app.core.config import settings
from app.database import db_session
from app.schemas.auth import TokenData, UserInDB
from app.models.user import User


PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_schema = OAuth2PasswordBearer(tokenUrl="access_token")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return PWD_CONTEXT.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return PWD_CONTEXT.hash(password)


def decode_token(token: str):
    try:
        decoded_token = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        return decoded_token if decoded_token['exp'] >= time.time() else None
    except:
        raise
        return {}


def create_access_token(*, sub: str) -> str:
    return _create_token(
        token_type="access_token",
        lifetime=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        sub=sub,
    )


def _create_token(
        token_type: str,
        lifetime: timedelta,
        sub: str) -> str:
    payload = {}
    expire = datetime.utcnow() + lifetime
    payload["type"] = token_type
    payload["exp"] = expire
    payload["iat"] = datetime.utcnow()
    payload["sub"] = str(sub)

    return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def get_current_user(db: Session = Depends(db_session), access_token: str = Depends(oauth2_schema)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validated credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = decode_token(access_token)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = db.query(User).filter(User.username == token_data.username).first()
    if user is None:
        raise credentials_exception
    return user


def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.status == "disabled":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user")
    return current_user


class RoleChecker:
    def __init__(self, allowed_roles: List):
        self.allowed_roles = allowed_roles

    def __call__(self, user: User = Depends(get_current_active_user)):
        if user.group_id not in self.allowed_roles:
            logger.debug(f"User with role {user.group_id} not in {self.allowed_roles}")
            raise HTTPException(status_code=403, detail="Operation not permitted")


'''
User roles settings
default (d), manager (m), admin (a), client (c)
'''
superuser = RoleChecker([1])
default = RoleChecker([1, 2, 3, 4])
manager = RoleChecker([1, 2])
admin = RoleChecker([1, 3])
client = RoleChecker([1, 4])
ma_role = RoleChecker([1, 2, 3])
mc_role = RoleChecker([1, 2, 4])
ac_role = RoleChecker([1, 3, 4])
