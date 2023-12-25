from typing import Optional
from fastapi import APIRouter, Request
from domain.customer import  models
from domain.payment import home
from domain.utils import general
from db.base import engine
from domain.utils.general import get_user_info
from api.models import StandardResponse
## from api.models import StandardResponse



router = APIRouter(
    prefix="/manager/payment",
    tags=["manager/payment"],
)

@router.get("/", status_code=200)
def Home() -> dict:
    """
    Root GET
    """
    return {"msg": "Hello, welcome to bookstore"}

@router.post("/buy/{order_id}")
async def create_order_endpoint(request: Request, order_id: int):
    with engine.begin() as conn:
        home.buy(conn, get_user_info(request), order_id)
        return StandardResponse.success_response({})
    
@router.get("/buy/get/")
async def get_bought_items_endpoint(request: Request):
    with engine.begin() as conn:
        return StandardResponse.success_response({
            "order_list": home.get_purchases(conn, get_user_info(request))
        })
    