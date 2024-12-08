from typing import List
from fastapi import APIRouter, Body, Header, Query, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from db.database import get_session
from exception.api_exception import DeleteIsNotAllowed, ParametersError
from exception.db_exception import ProductExists
from exception.login_exception import NotAuthToOps
from modules.login import permit_current_user
from modules.order import check_product_id_is_used
from modules.product import (
    create_product,
    delete_product,
    get_product_by_name,
    list_product_by_price,
    list_product_by_stock,
    modify_product,
)
from schemas.products import (
    ProductCreate,
    ProductCreateResponse,
    ProductList,
    ProductToDb,
    ProductUpdate,
)
from response.product_response import (
    create_product_response,
    delete_product_response,
    modify_product_response,
    get_product_response,
)
from schemas.users import UserRole

router = APIRouter()


@router.get(
    "/v1/product/price",
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
    if min_price > max_price:
        raise ParametersError(detail="Min price shouldn't bigger than max price")
    result = await list_product_by_price(min_price, max_price, db_session)
    await db_session.close()
    return result


@router.get(
    "/v1/product/stock",
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
    if min_stock > max_stock:
        raise ParametersError(detail="Min stock shouldn't bigger than max stock")
    result = await list_product_by_stock(min_stock, max_stock, db_session)
    await db_session.close()
    return result


@router.post(
    "/v1/product",
    status_code=status.HTTP_201_CREATED,
    include_in_schema=True,
    tags=["Product"],
    responses=create_product_response,
    response_model=ProductCreateResponse,
    summary="Create product API",
)
async def create_product_api(
    product: ProductCreate = Body(),
    token: str = Header(description="Your bearer token"),
    db_session: AsyncSession = Depends(get_session),
):
    user = await permit_current_user(token, db_session)
    if user.role != UserRole.MANAGER:
        raise NotAuthToOps()
    # validate pro
    db_product= await get_product_by_name(product.name, db_session)
    if db_product:
        raise ProductExists()
    product_to_db = ProductToDb(**product.model_dump(), creator_id=user.user_id)
    result = await create_product(product_to_db, db_session)
    await db_session.close()
    return result


@router.put(
    "/v1/product/{product_id}",
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
    token: str = Header(description="Your bearer token"),
    db_session: AsyncSession = Depends(get_session),
):
    user = await permit_current_user(token, db_session)
    if user.role != UserRole.MANAGER:
        raise NotAuthToOps()
    product_to_db = ProductToDb(**product_update.model_dump(), creator_id=user.user_id)
    result = await modify_product(product_to_db, product_id, db_session)
    await db_session.close()
    return result


@router.delete(
    "/v1/product/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    include_in_schema=True,
    tags=["Product"],
    responses=delete_product_response,
    summary="Delete product data API",
)
async def delete_product_api(
    product_id: int,
    token: str = Header(description="Your bearer token"),
    db_session: AsyncSession = Depends(get_session),
):
    await permit_current_user(token, db_session)
    db_result = await check_product_id_is_used(product_id, db_session)
    if db_result:
        raise DeleteIsNotAllowed(detail="An order has been placed for the product.")

    await delete_product(product_id, db_session)
    await db_session.close()
