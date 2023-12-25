from jsql import sql

from fastapi import  status
from domain.utils.general import UserInfo,OrderInfo
from domain.customer import models
from api import app

def buy(conn, user_info: UserInfo, order_id: int):

     sql(
        conn,
        """
            UPDATE `order`
            SET `purchased` = true
            WHERE order_id = :order_id AND customer_id = :customer_id
        """,
        order_id = order_id,
        customer_id = user_info.id
    )
    
def get_purchases(conn, user_info: UserInfo):
    data = sql(
        conn,
        """
            SELECT order_id, quantity, book_id
            FROM `order`
            WHERE `customer_id` = :customer_id AND `purchased` = true
        """,
        customer_id = user_info.id
    ).dicts()    
    return data