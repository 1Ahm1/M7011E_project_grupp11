from fastapi import APIRouter, Request
from db.base import engine
from api.models import StandardResponse
from domain.utils.general import get_user_info
from domain.admin import home
from domain.order.home import delete_order
router = APIRouter(
    prefix="/admin",
    tags=["admin"],
)

@router.get("/order/get/")
async def order_list_endpoint(request: Request):
    with engine.begin() as conn:
        assert home.is_admin(conn, get_user_info(request).id)
        return StandardResponse.success_response({
            "order_list": home.get_orders(conn)
        })
    
@router.delete("/order/delete/{order_id}")
async def delete_order_endpoint(request: Request, order_id: int):
    with engine.begin() as conn:
        delete_order(conn, get_user_info(request), order_id)
        return StandardResponse.success_response({})
    

@router.get("/customer/details/{customer_id}")
async def customer_details_endpoint(request: Request, customer_id: int):
    with engine.begin() as conn:
        return StandardResponse.success_response(
            home.customer_details(conn, customer_id)
        )

@router.get("/book/details/{book_id}")
async def book_details_endpoint(request: Request, book_id: int):
    with engine.begin() as conn:
        return StandardResponse.success_response(
            home.book_details(conn, book_id)
        )


