from pydantic import BaseModel
from typing import List

class CustomerInitData(BaseModel):
    user_id: int
    email: str = None
    phone_number: str = None
    name: str = None
    image_id: str = None
class CreateAccountRequest(BaseModel):
    user_id: int
    email: str = None
    phone_number: str = None
    name: str = None
    image_id: str = None
    password: str

class CreateBookRequest(BaseModel):
    name: str
    author: str
    description: str = None
    stock: int
    year: str
    price: float
    language: str
    

class CreateProductRequest(BaseModel):
    name: str
    price: int
    quantity: int
    book_id: int

class CreateOrderRequest(BaseModel):
    quantity: int
    book_id: int
    

class CreateManagerRequest(BaseModel):
    user_id: int
    company_permissions: str=None
    