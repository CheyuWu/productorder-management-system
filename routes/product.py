from typing import List
from fastapi import APIRouter, Query, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db.database import get_session
from modules.product import (
    create_product,
    delete_product,
    list_product_by_price,
    list_product_by_stock,
    modify_product,
)
from modules.user import get_user
from schemas.products import (
    ProductCreate,
    ProductCreateResponse,
    ProductList,
    ProductUpdate,
)
from response.product_response import (
    create_product_response,
    delete_product_response,
    modify_product_response,
    get_product_response,
)

router = APIRouter()


@router.get(
    "/product/price",
    status_code=status.HTTP_200_OK,
    include_in_schema=True,
    tags=["Product"],
    responses=get_product_response,
    response_model=List[ProductList],
    summary="Get product by price API",
)
async def list_product_price_api(
    min_price: float = Query(
        description="The min price",
        examples=["1.0"],
    ),
    max_price: float = Query(
        description="The max price",
        exampls=["1000.0"],
    ),
    db_session: AsyncSession = Depends(get_session),
):
    result = await list_product_by_price(min_price, max_price, db_session)
    await db_session.close()
    return result


@router.get(
    "/product/stock",
    status_code=status.HTTP_200_OK,
    include_in_schema=True,
    tags=["Product"],
    responses=get_product_response,
    response_model=List[ProductList],
    summary="Get product by stock API",
)
async def list_product_stock_api(
    min_stock: int = Query(
        description="The min stock",
        examples=["1"],
    ),
    max_stock: int = Query(
        description="The max stock",
        examples=["100"],
    ),
    db_session: AsyncSession = Depends(get_session),
):
    result = await list_product_by_stock(min_stock, max_stock, db_session)
    await db_session.close()
    return result


@router.post(
    "/product",
    status_code=status.HTTP_201_CREATED,
    include_in_schema=True,
    tags=["Product"],
    responses=create_product_response,
    response_model=ProductCreateResponse,
    summary="Create product API",
)
async def create_product_api(
    product: ProductCreate, db_session: AsyncSession = Depends(get_session)
):
    await get_user(product.creator_id, db_session)
    result = await create_product(product, db_session)
    await db_session.close()
    return result


@router.put(
    "/product/{product_id}",
    status_code=status.HTTP_200_OK,
    include_in_schema=True,
    tags=["Product"],
    responses=modify_product_response,
    response_model=ProductList,
    summary="Modify product data API",
)
async def modify_product_api(
    product_id: int,
    product_update: ProductUpdate,
    db_session: AsyncSession = Depends(get_session),
):
    result = await modify_product(product_id, product_update, db_session)
    await db_session.close()
    return result


@router.delete(
    "/product/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    include_in_schema=True,
    tags=["Product"],
    responses=delete_product_response,
    summary="Delete product data API",
)
async def delete_product_api(
    product_id: int,
    db_session: AsyncSession = Depends(get_session),
):
    await delete_product(product_id, db_session)
    await db_session.close()
