from typing import Optional
from fastapi import APIRouter, Request
from domain.customer import  models
from domain.product import home
from domain.utils import general
from db.base import engine
from domain.utils.general import get_user_info

## from api.models import StandardResponse



router = APIRouter(
    prefix="/manager/product",
    tags=["manager/product"],
)

@router.get("/", status_code=200)
def Home() -> dict:
    """
    Root GET
    """
    return {"msg": "Hello, welcome to bookstore"}

@router.post("/create/")
async def create_product_endpoint(request: Request, data: models.CreateProductRequest):
    with engine.begin() as conn:
        return home.create_product(conn, get_user_info(request), data)
    
@router.post("/delete/{product_id}")
async def delete_product_endpoint(request: Request, product_id: int):
    with engine.begin() as conn:
        return home.delete_product(conn, get_user_info(request), product_id)

@router.post("/search/{product_id}")
async def search_product_endpoint(request: Request, product_id: int):
    with engine.begin() as conn:
        return home.product_details(conn, get_user_info(request), product_id)

@router.get("/get/")
async def get_product_endpoint(request: Request):
    with engine.begin() as conn:
        return home.product_list(conn, get_user_info(request))