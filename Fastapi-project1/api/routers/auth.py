from http.client import HTTPException
from fastapi import APIRouter, Request
from domain.auth.main import login, activate_user, refresh, register_pending_user, resend_validation_code, update_password, reset_password, forgot_password, resend_password_code
from domain.auth.models import LoginRequest, RefreshRequest, RegisterPendingUserRequest, ActivateUserRequest, ResendCodeRequest, UpdatePasswordRequest, ResetPasswordRequest, ForgotPasswordRequest, ResendPasswordCodeRequest
from db.base import engine
from domain.user.account import get_user_profile
from api.models import StandardResponse
from domain.manager import home as manager_home
from domain.customer import home as customer_home
from domain.utils.general import get_user_info
from api.models import StandardResponse

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

@router.post("/register/")
async def register_endpoint(request: Request, data: RegisterPendingUserRequest):
    with engine.begin() as conn:
        return StandardResponse.success_response({
            "pending_user_id": register_pending_user(conn, request.state.current_user["lang"], data)
        })

@router.post("/token/")
async def login_endpoint(request: Request, data: LoginRequest):
    with engine.begin() as conn:
        user_profile, access_token, refresh_token = login(conn, request.state.current_user["lang"], data)

        return StandardResponse.success_response({
                "access_token": access_token,
                "refresh_token": refresh_token,
                "user_profile": user_profile
            })

@router.post("/refresh/")
async def refresh_endpoint(request: Request, data: RefreshRequest):
    with engine.begin() as conn:
        return StandardResponse.success_response({
            "access_token": refresh(conn, data.role, request.state.current_user["lang"], data.refresh_token)
        })

@router.post("/activate-user/")
async def validate_user_func(request: Request, data: ActivateUserRequest):
    with engine.begin() as conn:
        access_token, refresh_token = activate_user(conn, request.state.current_user["lang"], data)
        user_profile = get_user_profile(conn, phone_number = data.phone_number, email = data.email)

        return StandardResponse.success_response({
                "access_token": access_token,
                "refresh_token": refresh_token,
                "user_profile": user_profile
            })


@router.post("/resend-code/")
async def resend_code_func(request: Request, data: ResendCodeRequest):
    with engine.begin() as conn:
        resend_validation_code(conn, request.state.current_user["lang"], data)

@router.post("/password/update/")
async def update_password_endpoint(request: Request, data: UpdatePasswordRequest):
    with engine.begin() as conn:
        update_password(conn, request.state.current_user["lang"], data)

@router.post("/password/forgot-password/")
async def forgot_password_endpoint(request: Request, data: ForgotPasswordRequest):
    with engine.begin() as conn:
        role = forgot_password(conn, request.state.current_user["lang"], data)
        return {
                "role": role
            }

@router.post("/password/reset/")
async def reset_password_endpoint(request: Request, data: ResetPasswordRequest):
    with engine.begin() as conn:
        reset_password(conn, request.state.current_user["lang"], data)

@router.post("/password/resend-code/")
async def resend_password_code_endpoint(request: Request, data: ResendPasswordCodeRequest):
    with engine.begin() as conn:
        resend_password_code(conn, request.state.current_user["lang"], data)
