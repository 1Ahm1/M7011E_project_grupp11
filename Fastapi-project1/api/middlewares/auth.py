
from fastapi import Request, status
from fastapi.responses import JSONResponse
from domain.admin.admin import is_admin
from domain.utils.enums import MessageCode
from domain.utils.general import ENV
from domain.auth.security import validate_token_and_get_payload
from domain.utils.localization import get_message
from db.base import engine



def _is_protected_endpoint(url: str):
    # ToDo: check all protected endpoints
    protected_endpoint_prefixes = ["customer", "worker", "manager", "admin", "media", "user"]
    for prefix in protected_endpoint_prefixes:
        if url.startswith(f"/{prefix}/"): return True
    return False



def _authenticate_request_token(request: Request):
    if not _is_protected_endpoint(request.url.path): return { "id": None }
    token = request.headers.get("X-Token", None)
    if not token: token = request.cookies.get("X-Token", None)
    return validate_token_and_get_payload(token)


def auth_middleware(request: Request):
    lang = request.headers.get("lang", "en")
    try:
        payload = _authenticate_request_token(request)
    except Exception:
        return JSONResponse(
            content = {
                "success": False,
                "message": get_message(MessageCode.NOT_AUTHENTICATED, lang),
                "code": status.HTTP_401_UNAUTHORIZED
            },
            status_code = status.HTTP_200_OK
        )

    user_id = None
    if payload: user_id = payload.get("id", None)
    
    request.state.current_user = {
        "id": user_id,
        "lang": lang
    }

    if request.url.path.startswith("/admin/"):
        with engine.begin() as conn:
            if not is_admin(conn, user_id):
                return JSONResponse(
                    content = {
                        "success": False,
                        "message": get_message(MessageCode.NOT_FOUND, lang),
                        "code": status.HTTP_404_NOT_FOUND
                    },
                    status_code = status.HTTP_200_OK
                )







