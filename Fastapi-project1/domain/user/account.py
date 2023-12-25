
from domain.utils.general import UserInfo
from jsql import sql

from domain.user.models import UserProfile, UpdateProfileRequest
from domain.utils.localization import get_message
from fastapi import HTTPException, status
from domain.utils.enums import MessageCode
from typing import List


def get_user_profile(conn, *, email: str = None, phone_number: str = None, user_info: UserInfo = None) -> UserProfile:
    if not email and not user_info and not phone_number: return None
    data = sql(
        conn,
        """
            SELECT u.`user_id`, `email`, `phone_number`, `default_lang`, `default_role`, `name`
            FROM `user` u
            WHERE TRUE
            {% if user_id %}
                AND u.`user_id` = :user_id
            {% endif %}
            {% if email %}
                AND `email` = :email
            {% endif %}
            {% if phone_number %}
                AND `phone_number` = :phone_number
            {% endif %}
        """,
        user_id = None if not user_info else user_info.id,
        email = email,
        phone_number = phone_number
    ).dict()
    
    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=get_message(MessageCode.USER_NOT_FOUND, user_info.lang)
        )
    return UserProfile(**data)


def update_user_profile(conn, user_info: UserInfo, data: UpdateProfileRequest) -> UserProfile:
    data = sql(
        conn,
        """
            UPDATE `user`
            SET `user_id` = :user_id
            {% if default_lang %}
                ,`default_lang` = :default_lang
            {% endif %} 
            {% if default_role %}
                ,`default_role` = :default_role
            {% endif %} 
            {% if name %}
                ,`name` = :name
            {% endif %} 
            {% if image_id %}
                ,`image_id` = :image_id
            {% endif %} 
            WHERE `user_id` = :user_id
        """,
        user_id = user_info.id,
        default_lang = data.default_lang,
        default_role = data.default_role,
        name = data.name,
        image_id = data.image_id
    )
    
    return get_user_profile(conn, user_info = user_info)


