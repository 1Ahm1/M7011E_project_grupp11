from typing import Optional
from fastapi import APIRouter, Request
from domain.user import account, models
from db.base import engine
from pydantic import BaseModel
from domain.utils.general import get_user_info
from api.models import StandardResponse

router = APIRouter(
    prefix="/user",
    tags=["user"],
)

@router.get("/profile/get/")
async def init_endpoint(request: Request):
    with engine.begin() as conn:
        return StandardResponse.success_response(
            account.get_user_profile(conn, user_info = get_user_info(request))
            )
        



@router.post("/profile/update/")
async def init_endpoint(request: Request, data: models.UpdateProfileRequest):
    with engine.begin() as conn:
        account.update_user_profile(conn, get_user_info(request), data)
        return StandardResponse.success_response({})


