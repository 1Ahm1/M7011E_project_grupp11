from typing import Optional
from fastapi import APIRouter, Request
from domain.customer import  models
from domain.account import home
from domain.utils import general
from db.base import engine
from domain.utils.general import get_user_info

## from api.models import StandardResponse



RECIPES = [
    {
        "id": 1,
        "label": "Chicken Vesuvio",
        "source": "Serious Eats",
        "url": "http://www.seriouseats.com/recipes/2011/12/chicken-vesuvio-recipe.html",
    },
    {
        "id": 2,
        "label": "Chicken Paprikash",
        "source": "No Recipes",
        "url": "http://norecipes.com/recipe/chicken-paprikash/",
    },
    {
        "id": 3,
        "label": "Cauliflower and Tofu Curry Recipe",
        "source": "Serious Eats",
        "url": "http://www.seriouseats.com/recipes/2011/02/cauliflower-and-tofu-curry-recipe.html",
    },
]

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)

@router.get("/", status_code=200)
def Home() -> dict:
    """
    Root GET
    """
    return {"msg": "Hello, wellcome in bookstore"}

@router.post("/create-account/")
async def create_account_endpoint(request: Request, data: models.CreateAccountRequest):
    with engine.begin() as conn:
        return home.create_account(conn, get_user_info(request), data)
    
@router.post("/login/")
async def login_endpoint(request: Request, data: general.UserLogin):
    with engine.begin() as conn:
        return home.login_account(conn, get_user_info(request), data)