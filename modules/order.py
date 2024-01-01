import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from sqlmodel import col, select
from db.models import Order, OrderProduct, Product
from exception.api_exception import OutOfStock
from schemas.orders import OrderProductCreate, OrderProductModel
from sqlmodel.sql.expression import SelectOfScalar


async def create_order(
    customer_id: int, order_product_list: List[OrderProductCreate], db: AsyncSession
):
    # get all products
    product_ids = [order.product_id for order in order_product_list]
    select_statement = select(Product).where(col(Product.product_id).in_(product_ids))
    products = (await db.execute(select_statement)).scalars().all()

    # Create init orders
    order = Order(customer_id=customer_id, total_price=0)

    db_order_products: List[OrderProduct] = []
    # Calculate total price
    for order_product, product in zip(order_product_list, products):
        order_product = OrderProduct(
            order_id=order.order_id,
            product_id=order_product.product_id,
            quantity=order_product.quantity,
        )
        if product.stock < order_product.quantity:
            await db.rollback()
            raise OutOfStock()
        # substract the stock
        product.stock -= order_product.quantity
        db.add(product)
        # calculate total price
        order.total_price += product.price * order_product.quantity

        db.add(order_product)
        db_order_products.append(order_product)
    db.add(order)
    await db.commit()
    # update the data after transaction
    await db.refresh(order)
    refresh_tasks = [
        db.refresh(db_order_product) for db_order_product in db_order_products
    ]
    await asyncio.gather(*refresh_tasks)
    return order, db_order_products


async def check_product_id_is_used(product_id: int, db: AsyncSession):
    select_statement = select(OrderProduct).where(
        col(OrderProduct.product_id) == product_id
    )
    return (await db.execute(select_statement)).scalar_one_or_none()


async def list_order(customer_id: int, db: AsyncSession):
    select_statement = select(Order).where(col(Order.customer_id) == customer_id)
    return await get_orders_and_order_products(select_statement, db)


async def list_all_orders(db: AsyncSession):
    select_statement = select(Order)
    return await get_orders_and_order_products(select_statement, db)


async def get_orders_and_order_products(
    select_statement: SelectOfScalar[Order], db: AsyncSession
):
    order_results = (await db.execute(select_statement)).scalars().all()

    return [
        OrderProductModel(
            order_id=order.order_id,
            order_date=order.order_date,
            total_price=order.total_price,
            customer_id=order.customer_id,
            order_details=order.order_products,  # type:ignore
        )
        for order in order_results
    ]
