from fastapi import APIRouter, Depends, HTTPException, Response

from app.exception import IncorrectEmailOrPasswordException, UserAlreadyExistsException
from app.users.auth import *
from app.users.dao import UsersDAO
from app.users.dependies import get_current_user
from app.users.models import Users
from app.users.schemas import SUserAuth

router = APIRouter(
    prefix="/auth",
    tags=["Auth and Users"],
)


@router.post("/register")
async def register(user_data: SUserAuth):
    # Проверяем, существует ли пользователь
    user = await UsersDAO.find_one_or_none(email=user_data.email)
    if user:
        raise UserAlreadyExistsException()
    # Хешируем пароль
    hash_password = get_password_hash(password=user_data.password)
    new_user = await UsersDAO.add(email=user_data.email, hashed_password=hash_password)
    return {"message": f"{new_user.email} успешная регистрация id:{new_user.id}"}


@router.post("/login")
async def login(response: Response, user_data: SUserAuth):
    user = await auth_user(email=user_data.email, password=user_data.password)

    if not user:
        raise IncorrectEmailOrPasswordException()

    # Создаем JWT токен
    access_token = create_access_token(data={"sub": str(user.id)})
    response.set_cookie(
        "booking_access_token",
        access_token,
        httponly=True,  # Защита от XSS
        secure=False,  # Только HTTPS
        samesite="strict",  # Защита от CSRF
    )

    return access_token


@router.post("/logout")
async def logout(response: Response):
    response.delete_cookie("booking_access_token")
    return {"message": "вы вышли из системы"}


@router.get("/me")
async def me(user: Users = Depends(get_current_user)):
    return user
