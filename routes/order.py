from typing import List
from fastapi import APIRouter, Body, Header, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db.database import get_session
from exception.login_exception import NotAuthToOps
from modules.login import permit_current_user
from modules.order import create_order, list_all_orders, list_order
from modules.user import get_user_by_id
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
    token: str = Header(description="Your bearer token"),
    db_session: AsyncSession = Depends(get_session),
):
    user = await permit_current_user(token, db_session)
    if user.role != UserRole.CUSTOMER:
        raise NotAuthToOps()
    if user.role == UserRole.MANAGER:
        return await list_all_orders(db_session)
    else:
        return await list_order(user.user_id, db_session)


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
    token: str = Header(description="Your bearer token"),
    order_list: List[OrderProductCreate] = Body(),
    db_session: AsyncSession = Depends(get_session),
):
    user = await permit_current_user(token, db_session)
    if user.role != UserRole.CUSTOMER:
        raise NotAuthToOps()
    order, order_details = await create_order(user.user_id, order_list, db_session)
    await db_session.close()
    
    return OrderProductModel(
        order_id=order.order_id,
        customer_id=order.customer_id,
        order_date=order.order_date,
        total_price=order.total_price,
        order_details=order_details,  # type:ignore
    )
