from jsql import sql

from fastapi import  status
from domain.utils.general import UserInfo,OrderInfo
from domain.customer import models
from api import app

def create_order(conn, user_info: UserInfo, data: models.CreateOrderRequest):

    stock = sql(
        conn,
        """
            SELECT `stock` FROM `book`
            WHERE book_id = :book_id 
        """,
        book_id = data.book_id
    ).scalar()

    if data.quantity > stock:
        return "Not enough in stock"
    
    sql(
        conn,
        """
            UPDATE `book`
            SET `stock` = :stock
            WHERE book_id = :book_id 
        """,
        stock = stock - data.quantity,
        book_id = data.book_id
    )

    sql(
        conn,
        """
            Insert INTO `order` (quantity, book_id, customer_id)
            VALUES (:quantity, :book_id, :customer_id)
        """,
        quantity = data.quantity,
        book_id = data.book_id,
        customer_id = user_info.id
    ).lastrowid
    

def delete_order(conn, user_info: UserInfo, order_id):

    details = sql(
        conn,
        """
            SELECT `quantity`, `book_id` FROM `order`
            WHERE `order_id` = :id
        """,
        id = order_id
        
    ).dict()
    sql(
        conn,
        """
            UPDATE `book`
            SET `stock` = :quantity + `stock`
            WHERE `book_id` = :book_id
        """,
        book_id = details['book_id'],
        quantity = details['quantity']
        
    )
    sql(
        conn,
        """
            DELETE FROM `order`
            WHERE `order_id` = :id
        """,
        id = order_id
        
    ).lastrowid
    
    
def order_details(conn, user_info: UserInfo, order_id):
    data = sql(
        conn,
        """
            SELECT order_id, quantity, book_id
            FROM `order`
            WHERE order_id =:order_id 
        """,
        order_id = order_id
    ).dict()    
    return data

def order_list(conn, user_info: UserInfo):
    data = sql(
        conn,
        """
            SELECT order_id, quantity, book_id
            FROM `order`
            WHERE `customer_id` = :customer_id AND `purchased` = false
        """,
        customer_id = user_info.id
    ).dicts()    
    return data