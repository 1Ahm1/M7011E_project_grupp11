from typing import Optional
from fastapi import APIRouter, Request
from domain.customer import home, models
from db.base import engine
from pydantic import BaseModel

## from api.models import StandardResponse



router = APIRouter(
    prefix="/customer",
    tags=["customer"],
)
class UserInfo(BaseModel):
    id: int
    role: str = "customer"
    lang: str
    
def get_user_info(request, role = "customer"):
    return UserInfo(
        id = request.state.current_user["id"],
        role = role,
        lang = request.state.current_user["lang"]
    )
@router.get("/", status_code=200)
def Home() -> dict:
    """
    Root GET
    """
    return {"msg": "Hello, wellcome in bookstore"}

@router.get("/init/", response_model = Optional[models.CustomerInitData])
async def init_endpoint(request: Request):
    with engine.begin() as conn:
        return home.get_init_data(conn, get_user_info(request).id)




