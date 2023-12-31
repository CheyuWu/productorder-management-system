from typing import List
from uuid import UUID
from fastapi import APIRouter, Query, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db.database import get_session
from response.order_response import get_order_response, create_order_response
from schemas.orders import OrderProductCreate


router = APIRouter()


@router.get(
    "/order/",
    status_code=status.HTTP_200_OK,
    include_in_schema=True,
    tags=["Order"],
    responses=get_order_response,
    # response_model=List[ProductList],
    summary="Get order API",
)
async def list_order_api(
    order_id: UUID, db_session: AsyncSession = Depends(get_session)
):
    pass


@router.post(
    "/order/",
    status_code=status.HTTP_201_CREATED,
    include_in_schema=True,
    tags=["Order"],
    responses=create_order_response,
    # response_model=List[ProductList],
    summary="Create order API",
)
async def create_order_api(
    customer_id: int,
    order_list: List[OrderProductCreate],
    db_session: AsyncSession = Depends(get_session),
):
    pass
