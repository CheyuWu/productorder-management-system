from typing import List
from fastapi import APIRouter, Body, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db.database import get_session
from modules.order import create_order, list_all_orders, list_order
from modules.user import get_user
from response.order_response import get_order_response, create_order_response
from schemas.orders import OrderProductCreate, OrderProductModel
from schemas.users import UserRole


router = APIRouter()


@router.get(
    "/order/",
    status_code=status.HTTP_200_OK,
    include_in_schema=True,
    tags=["Order"],
    responses=get_order_response,
    response_model=List[OrderProductModel],
    summary="Get order API",
)
async def list_order_api(
    customer_id: int, db_session: AsyncSession = Depends(get_session)
):
    User = await get_user(customer_id, db_session)
    if User.role == UserRole.MANAGER:
        return await list_all_orders(db_session)
    else:
        return await list_order(User.user_id, db_session)


@router.post(
    "/order/",
    status_code=status.HTTP_201_CREATED,
    include_in_schema=True,
    tags=["Order"],
    responses=create_order_response,
    response_model=OrderProductModel,
    summary="Create order API",
)
async def create_order_api(
    customer_id: int = Body(),
    order_list: List[OrderProductCreate] = Body(),
    db_session: AsyncSession = Depends(get_session),
):
    await get_user(customer_id, db_session)
    order, order_details = await create_order(customer_id, order_list, db_session)
    await db_session.close()
    return OrderProductModel(
        order_id=order.order_id,
        customer_id=order.customer_id,
        order_date=order.order_date,
        total_price=order.total_price,
        order_details=order_details,  # type:ignore
    )
