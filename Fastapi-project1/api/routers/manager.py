from typing import Optional
from fastapi import APIRouter, Request
from domain.customer import  models
from domain.manager import home
from domain.utils import general
from db.base import engine
from domain.utils.general import get_user_info

## from api.models import StandardResponse



router = APIRouter(
    prefix="/manager",
    tags=["manager"],
)

@router.get("/", status_code=200)
def Home() -> dict:
    """
    Root GET
    """
    return {"msg": "Hello, wellcome in bookstore"}

@router.post("/create_account/")
async def create_Manager_account_endpoint(request: Request, data: models.CreateManagerRequest):
    with engine.begin() as conn:
        return home.create_account(conn, get_user_info(request), data)
    
@router.post("/delet/{manager_id}")
async def delete_order_endpoint(request: Request, manager_id: int):
    with engine.begin() as conn:
        return home.delet_manager(conn, get_user_info(request), manager_id)

@router.post("/search/{manager_id}")
async def search_order_endpoint(request: Request, manager_id: int):
    with engine.begin() as conn:
        return home.manager_details(conn, get_user_info(request), manager_id)