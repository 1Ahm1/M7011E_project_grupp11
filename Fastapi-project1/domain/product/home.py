from jsql import sql

from fastapi import  status
from domain.utils.general import UserInfo,BookInfo,ProductInfo
from domain.customer import models
from api import app

def create_product(conn, user_info: UserInfo, data: models.CreateProductRequest):

    is_here = sql(
        conn,
        """
            SELECT COUNT(*) FROM `product`
            WHERE `name` = :name
        """,
        name = data.name
    ).scalar()
    if is_here == 0:
        sql(
        conn,
        """
            Insert INTO product (price, quantity, book_id,name)
            VALUES (:price, :quantity, :book_id, :name)
        """,
        price = data.price,
        quantity = data.quantity,
        book_id = data.book_id, 
        name=data.name
    ).lastrowid
    

def delete_product(conn, user_info: UserInfo, product_id):

    sql(
        conn,
        """
            DELETE FROM product
            WHERE `product_id` = :id
        """,
        id = product_id
        
    ).lastrowid
    
def product_details(conn, user_info: UserInfo, product_id):
    data = sql(
        conn,
        """
            SELECT product_id, name, price, quantity, book_id
            FROM product
            WHERE product_id =:product_id 
        """,
        product_id = product_id
    ).dict()    
    return data

def product_list(conn, user_info: UserInfo):
    data = sql(
        conn,
        """
            SELECT product_id, name, price, quantity, book_id
            FROM product
        """
    ).dicts()    
    return data