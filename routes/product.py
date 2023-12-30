from typing import Dict, Union
from fastapi import APIRouter, Header, status

from schemas.products import ProductCreate


router = APIRouter()

responses: Dict[Union[int, str], Dict[str, str]] = {
    400: {"description": "You missed some parameters or paramters was not corrected"},
    403: {"description": "The data does not exists"},
    500: {"description": "Unknown error"},
}


@router.post(
    "/product",
    status_code=status.HTTP_201_CREATED,
    include_in_schema=True,
    tags=["Products"],
    responses=responses,
    response_model=ProductCreate,
    summary="Create product API",
)
async def create_product(
    name: str = Header(
        description="Your product name",
        example="Banana",
    ),
    price: float = Header(
        description="Your product price",
        example="100",
    ),
    stock: int = Header(description="Your product stock", example="10"),
):
    """
    Create products
    """
    pass


@router.put("/product")
async def modify_product():
    """
    Modify product
    """
    pass


@router.delete("/product")
async def delete_product():
    """ """
    pass
