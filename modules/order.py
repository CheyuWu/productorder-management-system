from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from schemas.orders import OrderProductCreate


async def create_order(
    customer_id: int, order_list: List[OrderProductCreate], db_session: AsyncSession
):
    pass
