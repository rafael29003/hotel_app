from datetime import datetime, timezone

from fastapi import Depends, Request
from jose import JWTError, jwt
from pydantic_core.core_schema import str_schema

from app.config import settings
from app.exception import (
    ExpiredTokenException,
    IncorrectTokenFormatException,
    TokenAbsentException,
    UserIsNotPresentException,
)
from app.users.dao import UsersDAO


def get_token(request: Request):
    token = request.cookies.get("booking_access_token")
    if not token:
        raise TokenAbsentException()
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
    except JWTError:
        raise IncorrectTokenFormatException()

    expire = payload.get("exp")
    if expire and expire > datetime.now(timezone.utc).timestamp():
        user_id = int(payload.get("sub"))
    else:
        raise ExpiredTokenException()

    if not user_id:
        raise UserIsNotPresentException()

    user = await UsersDAO.find_by_id(user_id)
    if not user:
        raise UserIsNotPresentException()

    return user
