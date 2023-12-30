from fastapi import APIRouter, status, Depends
from db.database import get_session
from modules.user import create_user
from response.user_response import create_user_response
from schemas.users import UserBase, UserCreate
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.post(
    "/user",
    status_code=status.HTTP_201_CREATED,
    include_in_schema=True,
    tags=["Products"],
    responses=create_user_response,
    response_model=UserBase,
    summary="Create user API",
)
async def create_user_api(
    user_model: UserCreate, db_session: AsyncSession = Depends(get_session)
):
    return await create_user(user_model, db_session)
