
from jsql import sql
from domain.auth import communication, security
from domain.auth.models import LoginRequest, RegisterPendingUserRequest, ActivateUserRequest, ResendCodeRequest, UpdatePasswordRequest, ResetPasswordRequest, ForgotPasswordRequest, ResendPasswordCodeRequest
from domain.user.account import get_user_profile
from domain.utils.general import UserInfo, is_valid_email, is_valid_phone_number
from domain.utils.enums import MessageCode
from domain.utils.localization import get_message
from fastapi import Request, status, HTTPException

MAX_CODE_RESEND_ATTEMPTS = 5

def _validate_user_input(lang: str, *, email: str = None, phone_number: str = None):
    if email and phone_number is None:
        if not is_valid_email(email):
            raise HTTPException(
                status_code = status.HTTP_400_BAD_REQUEST,
                detail = get_message(MessageCode.INVALID_EMAIL, lang)
            )
        return email
    elif phone_number and email is None:
        if not is_valid_phone_number(phone_number):
            raise HTTPException(
                status_code = status.HTTP_400_BAD_REQUEST,
                detail = get_message(MessageCode.INVALID_PHONE_NUMBER, lang)
            )
        return phone_number
    else:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = get_message(MessageCode.INVALID_USER_INPUT, lang)
        )


def _email_exists(conn, email: str):
    exists = sql(
        conn,
        """SELECT COUNT(*) FROM `user` WHERE `email` = :email""",
        email = email
    ).scalar()
    return exists > 0
    
def _phone_number_exists(conn, phone_number: str):
    exists = sql(
        conn,
        """SELECT COUNT(*) FROM `user` WHERE `phone_number` = :phone_number""",
        phone_number = phone_number
    ).scalar()
    return exists > 0


def _validate_user_password(conn, password: str, *, email: str = None, phone_number: str = None) -> bool:
    assert email or phone_number
    data = sql(
        conn,
        """
            select `password_hash`, `salt`
            from `user` u 
            where TRUE
            {% if email %}
                AND `email` = :email
            {% endif %}
            {% if phone_number %}
                AND `phone_number` = :phone_number
            {% endif %}
        """,
        email = email,
        phone_number = phone_number
    ).dict()

    if not data: return False

    return security.validate_password(
        provided_password = password,
        stored_password_hash = data["password_hash"],
        salt = data["salt"]
    )


def register_pending_user(conn, lang: str, data: RegisterPendingUserRequest):
    if not security.is_strong_password(data.password, data.role):
        raise HTTPException(detail = get_message(MessageCode.NOT_STRONG_PASSWORD, lang), status_code = status.HTTP_400_BAD_REQUEST)
        
    username = _validate_user_input(lang, email = data.email, phone_number = data.phone_number)

    if data.email and _email_exists(conn, data.email):
        raise HTTPException(detail = get_message(MessageCode.EMAIL_ALREADY_EXISTS, lang), status_code = status.HTTP_400_BAD_REQUEST)
    if data.phone_number and _phone_number_exists(conn, data.phone_number):
        raise HTTPException(detail = get_message(MessageCode.PHONE_NUMBER_ALREADY_EXISTS, lang), status_code = status.HTTP_400_BAD_REQUEST)
    

    password_hash, salt = security.hash_password_and_get_salt(data.password)
    validation_code = communication.generate_validation_code()

    pending_user_id = sql(
        conn,
        """
            INSERT INTO `pending_user`(`email_or_phone_number`, `name`, `validation_code`, `password_hash`, `salt`, `default_lang`, `role`)
            VALUES (:email_or_phone_number, :name, :validation_code, :password_hash, :salt, :default_lang, :role)
        """,
        email_or_phone_number = username,
        name = data.name,
        validation_code = validation_code,
        password_hash = password_hash,
        salt = salt,
        default_lang = lang,
        role = data.role
    ).lastrowid

    if data.email: communication.send_code_to_email(username, validation_code)
    if data.phone_number: communication.send_code_to_phone_number(username, validation_code)
    
    return pending_user_id
    
def resend_validation_code(conn, lang: str, data: ResendCodeRequest):
    username = data.email or data.phone_number
    assert username

    pending_user_info = sql(
        conn,
        """
            SELECT `validation_code`, `code_resend_attempts`
            FROM `pending_user`
            WHERE `pending_user_id` = :pending_user_id
                AND `email_or_phone_number` = :username
        """,
        username = username,
        pending_user_id = data.pending_user_id,
        attempts_limit = MAX_CODE_RESEND_ATTEMPTS
    ).dict()
    
    if not pending_user_info:
        raise HTTPException(detail = get_message(MessageCode.USER_NOT_FOUND, lang), status_code = status.HTTP_400_BAD_REQUEST)

    validation_code, attempts = pending_user_info["validation_code"], pending_user_info["code_resend_attempts"] + 1
    
    if attempts > MAX_CODE_RESEND_ATTEMPTS:
        raise HTTPException(detail = get_message(MessageCode.RESEND_ATTEMPTS_LIMIT, lang), status_code = status.HTTP_400_BAD_REQUEST)

    sql(
        conn,
        """
            UPDATE `pending_user`
            SET `code_resend_attempts` = :attempts
            WHERE `pending_user_id` = :pending_user_id
                AND `email_or_phone_number` = :username 
        """,
        attempts = attempts,
        pending_user_id = data.pending_user_id,
        username = username
    )

    if data.email: communication.send_code_to_email(data.email, validation_code)
    elif data.phone_number: communication.send_code_to_phone_number(data.phone_number, validation_code)

def login(conn, lang, data: LoginRequest):
    
    user_profile = get_user_profile(conn, email = data.email, phone_number = data.phone_number)

    if not security.is_strong_password(data.password, user_profile.default_role):
        raise HTTPException(detail = get_message(MessageCode.NOT_STRONG_PASSWORD, lang), status_code = status.HTTP_400_BAD_REQUEST)
    
    _validate_user_input(lang, email = data.email, phone_number = data.phone_number)

    if not _validate_user_password(conn, data.password, email = data.email, phone_number = data.phone_number):
        raise HTTPException(detail = get_message(MessageCode.INVALID_USERNAME_OR_PASSWORD, lang), status_code = status.HTTP_400_BAD_REQUEST)

    access_token = security.generate_token(conn, user_profile.user_id, role = user_profile.default_role)
    refresh_token = security.generate_token(conn, user_profile.user_id, role = user_profile.default_role, is_refresh_token = True)
    
    return user_profile, access_token, refresh_token
    

def activate_user(conn, lang: str, data: ActivateUserRequest):
    assert data.role in ["customer", "admin", "manager"], "invalid-role"
    _validate_user_input(lang, email = data.email, phone_number = data.phone_number)
    pending_user = sql(
        conn,
        f"""
            SELECT *
            FROM `pending_user`
            WHERE `pending_user_id` = :pending_user_id
                AND `email_or_phone_number` = :email_or_phone_number
                AND `validation_code` = :validation_code
                AND `role` = :role
        """,
        pending_user_id = data.pending_user_id,
        validation_code = data.validation_code,
        role = data.role,
        email_or_phone_number = data.email if data.email else data.phone_number
    ).dict()

    if not pending_user:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = get_message(MessageCode.INVALID_CODE, lang)
        )

    row_count = sql(
        conn,
        f"""
            DELETE FROM `pending_user`
            WHERE `pending_user_id` = :pending_user_id
        """,
        pending_user_id = data.pending_user_id
    ).rowcount
    assert row_count == 1


    user_id = sql(
        conn,
        f"""
            INSERT INTO `user` (`email`, `phone_number`, `password_hash`, `salt`, `default_lang`, `default_role`, `name`)
            VALUES (:email, :phone_number, :password_hash, :salt, :default_lang, :role, :name)
        """,
        **pending_user,
        email = data.email,
        phone_number = data.phone_number
    ).lastrowid

    account_roles = []
    account_roles.append(data.role)
    for r in account_roles:
        sql(
            conn,
            f"""
                INSERT INTO `{r}` (`user_id`)
                VALUES (:user_id)
            """,
            user_id = user_id
        )

    access_token = security.generate_token(conn, user_id, role = data.role)
    refresh_token = security.generate_token(conn, user_id, role = data.role, is_refresh_token = True)
    
    return access_token, refresh_token


def refresh(conn, role: str, lang: str, refresh_token: str):
    try:
        payload = security.validate_token_and_get_payload(refresh_token, conn, is_refresh_token = True)
        user_id = int(payload["id"])
        assert user_id
        return security.generate_token(conn, user_id, role = role)
    except Exception as e:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = get_message(MessageCode.INVALID_TOKEN, lang)
        )

def update_password(conn, lang, data: UpdatePasswordRequest):
    if not security.is_strong_password(data.new_password, data.role):
        raise HTTPException(detail = get_message(MessageCode.NOT_STRONG_PASSWORD, lang), status_code = status.HTTP_400_BAD_REQUEST)
    
    _validate_user_input(lang, email = data.email, phone_number = data.phone_number)

    if not _validate_user_password(conn, data.old_password, email = data.email, phone_number = data.phone_number):
        raise HTTPException(detail = get_message(MessageCode.INVALID_PASSWORD, lang), status_code = status.HTTP_400_BAD_REQUEST)
    
    if _validate_user_password(conn, data.new_password, email = data.email, phone_number = data.phone_number):
        raise HTTPException(detail = get_message(MessageCode.CANNOT_USE_SAME_PASSWORD, lang), status_code = status.HTTP_400_BAD_REQUEST)

    user_profile = get_user_profile(conn, email = data.email, phone_number = data.phone_number)
    password_hash, salt = security.hash_password_and_get_salt(data.new_password)
    security.change_password(conn, user_profile.user_id, password_hash, salt)

def forgot_password(conn, lang, data: ForgotPasswordRequest):
        
    _validate_user_input(lang, email = data.email, phone_number = data.phone_number)
    validation_code = communication.generate_validation_code()

    user_profile = get_user_profile(conn, email = data.email, phone_number = data.phone_number)

    sql(
        conn,
        """
            INSERT INTO `reset_password`(`user_id`, `email`, `phone_number`, `validation_code`)
            VALUES (:user_id, :email, :phone_number, :validation_code)
        """,
        user_id = user_profile.user_id,
        email = data.email,
        phone_number = data.phone_number,
        validation_code = validation_code,
    )

    if data.email: communication.send_code_to_email(data.email, validation_code)
    if data.phone_number: communication.send_code_to_phone_number(data.phone_number, validation_code)

    return user_profile.default_role
    
def reset_password(conn, lang, data: ResetPasswordRequest):
    if not security.is_strong_password(data.new_password, data.role):
        raise HTTPException(detail = get_message(MessageCode.NOT_STRONG_PASSWORD, lang), status_code = status.HTTP_400_BAD_REQUEST)
    
    _validate_user_input(lang, email = data.email, phone_number = data.phone_number)

    if not security.validate_reset_code(conn, data.validation_code, email = data.email, phone_number = data.phone_number):
        raise HTTPException(detail = get_message(MessageCode.INVALID_CODE, lang), status_code = status.HTTP_400_BAD_REQUEST)
    
    user_profile = get_user_profile(conn, email = data.email, phone_number = data.phone_number)
    password_hash, salt = security.hash_password_and_get_salt(data.new_password)
    security.change_password(conn, user_profile.user_id, password_hash, salt)

def resend_password_code(conn, lang: str, data: ResendPasswordCodeRequest):

    _validate_user_input(lang, email = data.email, phone_number = data.phone_number)

    user_profile = get_user_profile(conn, email = data.email, phone_number = data.phone_number)

    info = sql(
        conn,
        """
            SELECT `validation_code`, `code_resend_attempts`
            FROM `reset_password`
            WHERE `user_id` = :user_id
            {% if email %}
                AND `email` = :email
            {% endif %}
            {% if phone_number %}
                AND `phone_number` = :phone_number
            {% endif %}
        """,
        user_id = user_profile.user_id,
        email = data.email,
        phone_number = data.phone_number
    ).dict()
    
    if not info:
        raise HTTPException(detail = get_message(MessageCode.USER_NOT_FOUND, lang), status_code = status.HTTP_404_NOT_FOUND)

    validation_code, attempts = info["validation_code"], info["code_resend_attempts"] + 1
    
    if attempts > MAX_CODE_RESEND_ATTEMPTS:
        raise HTTPException(detail = get_message(MessageCode.RESEND_ATTEMPTS_LIMIT, lang), status_code = status.HTTP_400_BAD_REQUEST)

    sql(
        conn,
        """
            UPDATE `reset_password`
            SET `code_resend_attempts` = :attempts
            WHERE `user_id` = :user_id
            {% if email %}
                AND `email` = :email
            {% endif %}
            {% if phone_number %}
                AND `phone_number` = :phone_number
            {% endif %}
        """,
        user_id = user_profile.user_id,
        email = data.email,
        phone_number = data.phone_number,
        attempts = attempts
    )

    if data.email: communication.send_code_to_email(data.email, validation_code)
    elif data.phone_number: communication.send_code_to_phone_number(data.phone_number, validation_code)