from typing import Annotated
from fastapi import Depends
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from core import get_settings
from exception.login_exception import NotAuthCurrentUser
from modules.user import get_user_by_name
from datetime import datetime, timedelta
from jose import JWTError, jwt


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = get_settings().SECRET_KEY
ALGORITHM = get_settings().ENCRYPT_ALGORITHM


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str):
    return pwd_context.hash(password)


async def authenticate_user(username: str, password: str, db: AsyncSession):
    user = await get_user_by_name(username, db)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


async def permit_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: AsyncSession,
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub", None)
        if username is None:
            raise NotAuthCurrentUser()
    except JWTError:
        raise NotAuthCurrentUser()
    user = await get_user_by_name(username, db)
    if user is None:
        raise NotAuthCurrentUser()
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
