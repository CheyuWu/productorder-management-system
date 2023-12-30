from fastapi import APIRouter, status, Depends
from db.database import get_session
from modules.user import create_user, delete_user
from response.user_response import create_user_response, delete_user_response
from schemas.users import UserBase, UserCreate, UserDelete
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.post(
    "/user",
    status_code=status.HTTP_201_CREATED,
    include_in_schema=True,
    tags=["User"],
    responses=create_user_response,
    response_model=UserBase,
    summary="Create user API",
)
async def create_user_api(
    user_model: UserCreate, db_session: AsyncSession = Depends(get_session)
):
    response = await create_user(user_model, db_session)
    await db_session.close()
    return response


@router.delete(
    "/user",
    status_code=status.HTTP_204_NO_CONTENT,
    include_in_schema=True,
    tags=["User"],
    responses=delete_user_response,
    summary="Delete user API",
)
async def delete_user_api(
    user_model: UserDelete, db_session: AsyncSession = Depends(get_session)
):
    await delete_user(user_model.username, db_session)
    await db_session.close()
