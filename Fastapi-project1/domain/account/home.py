from jsql import sql

from fastapi import  status
from domain.utils.general import UserInfo,UserLogin
from api import app
def create_account(conn, data: UserInfo):

    is_user = sql(
        conn,
        """
            SELECT COUNT(*) FROM `user`
            WHERE `user_id` = :user_id
        """,
        user_id = data.id
    ).scalar()
    if is_user == 0:
        sql(
        conn,
        """
            Insert INTO user (user_id, name, email, image_id, phone_number, password)
            VALUES (:user_id, :name, :email, :image_id, :phone_number, :password)
        """,
        user_id = data.id,
        name = data.name,
        phone_number = data.phone_number,
        image_id = data.image_id,
        email = data.email,
        password = data.password
    ).lastrowid
    

def login_account(conn, data: UserLogin):

    is_user = sql(
        conn,
        """
            SELECT user_id FROM `user`
            WHERE `email` = :email AND `password` = :password
        """,
        email = data.email,
        password=data.password
    ).scalar()
    if is_user != 0:
        app.user_now=is_user
        return is_user
    
    

