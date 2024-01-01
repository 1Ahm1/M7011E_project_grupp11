
from jsql import sql
from domain.utils.general import UserInfo


def is_admin(conn, user_id: int) -> bool:
    data = sql(
        conn,
        "SELECT `is_active` FROM `admin` WHERE `user_id` = :user_id",
        user_id = user_id
    ).dict()
    if not data or not data["is_active"]: return False
    return bool(data["is_active"])

def get_orders(conn):

    data = sql(
        conn,
        """
            SELECT `order_id`, `quantity`, `book_id`, `customer_id`
            FROM `order`
            WHERE `purchased` = false
        """
    ).dicts()
    return data

def book_details(conn, book_id):

    data = sql(
        conn,
        """
            SELECT book_id, name, author, description, image.url as image, language, year, price, stock
            FROM book
            LEFT JOIN image ON image.image_id = book.image_id
            WHERE book_id =:book_id 
        """,
        book_id = book_id
    ).dict()
    return data

def customer_details(conn, user_id):

    data = sql(
        conn,
        """
            SELECT user_id, email, name
            FROM `user`
            WHERE user_id = :user_id
        """,
        user_id = user_id
    ).dict()
    return data







