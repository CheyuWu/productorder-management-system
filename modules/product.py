from sqlalchemy import delete, update
from sqlmodel import col, select
from db.models import Product
from exception.db_exception import ProductNotFound
from schemas.products import ProductCreate, ProductUpdate
from sqlalchemy.ext.asyncio import AsyncSession


async def list_product_by_price(min_price: float, max_price: float, db: AsyncSession):
    select_statement = select(Product).where(
        col(Product.price) >= min_price, col(Product.price) <= max_price
    )
    return (await db.execute(select_statement)).scalars().all()


async def list_product_by_stock(min_stock: int, max_stock: int, db: AsyncSession):
    select_statement = select(Product).where(
        col(Product.stock) >= min_stock, col(Product.stock) <= max_stock
    )
    return (await db.execute(select_statement)).scalars().all()


async def get_product_by_id(product_id: int, db: AsyncSession):
    select_statement = select(Product).where(col(Product.product_id) == product_id)
    db_product = (await db.execute(select_statement)).scalar_one_or_none()
    if not db_product:
        raise ProductNotFound()
    return db_product


async def create_product(product: ProductCreate, db: AsyncSession):
    product_to_db = Product.model_validate(product)
    db.add(product_to_db)
    await db.commit()
    await db.refresh(product_to_db)
    return product_to_db


async def modify_product(
    product_id: int, product_update: ProductUpdate, db: AsyncSession
):
    db_product = await get_product_by_id(product_id, db)
    product_data = product_update.model_dump(exclude_unset=True)
    for key, value in product_data.items():
        setattr(db_product, key, value)
    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)
    return db_product


async def delete_product(product_id: int, db: AsyncSession):
    await get_product_by_id(product_id, db)
    delete_statement = delete(Product).where(col(Product.product_id) == product_id)
    await db.execute(delete_statement)
    await db.commit()
