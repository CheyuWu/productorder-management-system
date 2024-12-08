from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, status, Depends
from core import get_settings
from exception.login_exception import NotAuthCurrentUser
from modules.login import authenticate_user, create_access_token
from db.database import get_session
from response.login_response import get_login_response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.login import loginResp

router = APIRouter()

ACCESS_TOKEN_EXPIRE_MINUTES = get_settings().ACCESS_TOKEN_EXPIRE_MINUTES


@router.post(
    "/v1/login",
    status_code=status.HTTP_200_OK,
    include_in_schema=True,
    tags=["Login"],
    responses=get_login_response,
    response_model=loginResp,
    summary="Get order API",
)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db_session: AsyncSession = Depends(get_session),
):
    user = await authenticate_user(form_data.username, form_data.password, db_session)
    if not user:
        raise NotAuthCurrentUser()
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    await db_session.close()
    return loginResp(access_token=access_token, token_type="bearer")
