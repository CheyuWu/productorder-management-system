from fastapi import APIRouter, status, Depends
from db.database import get_session
from modules.user import create_user, delete_user
from response.user_response import create_user_response, delete_user_response
from schemas.users import UserBase, UserCreate, UserCreateResponse, UserDelete
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.post(
    "/user",
    status_code=status.HTTP_201_CREATED,
    include_in_schema=True,
    tags=["User"],
    responses=create_user_response,
    response_model=UserCreateResponse,
    summary="Create user API",
)
async def create_user_api(
    user: UserCreate, db_session: AsyncSession = Depends(get_session)
):
    result = await create_user(user, db_session)
    await db_session.close()
    return result


@router.delete(
    "/user/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    include_in_schema=True,
    tags=["User"],
    responses=delete_user_response,
    summary="Delete user API",
)
async def delete_user_api(
    user_id: int, db_session: AsyncSession = Depends(get_session)
):
    await delete_user(user_id, db_session)
    await db_session.close()
