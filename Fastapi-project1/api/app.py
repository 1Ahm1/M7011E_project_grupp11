from fastapi import FastAPI, Request, HTTPException, Response, status, APIRouter
from api.routers import customer,auth,book,order,manager, payment, user, admin
from api.middlewares.auth import auth_middleware
from fastapi.responses import RedirectResponse, PlainTextResponse, JSONResponse
import traceback

app = FastAPI(title="Recipe API", openapi_url="/openapi.json")
user_now=0

# notice: when creating a new router file under /routers folder, add it here




@app.middleware("http")
async def middleware(request: Request, call_next):
    lang = request.headers.get("lang", "en")
    auth_middleware(request)
    
    try:
        return await call_next(request)
    except Exception as e:
        error_stack = traceback.format_exc()
        # ToDo: check before production
        return JSONResponse(
            content = {
                "success": False,
                "message": "internal server error",
                "exception": error_stack,
                "code": status.HTTP_401_UNAUTHORIZED
            },
            status_code = status.HTTP_200_OK
        )


app.include_router(customer.router)
app.include_router(auth.router)
app.include_router(book.router)
app.include_router(order.router)
app.include_router(manager.router)
app.include_router(payment.router)
app.include_router(user.router)
app.include_router(admin.router)



##app.include_router(auth.router)


