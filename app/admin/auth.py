from sqladmin import Admin
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse

from app.config import settings
from app.exception import IncorrectEmailOrPasswordException
from app.users.auth import auth_user, create_access_token
from app.users.dependies import get_current_user
from app.users.models import Users


class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        email, password = form["username"], form["password"]
        user = await auth_user(email=email, password=password)

        if user:
            access_token = create_access_token(data={"sub": str(user.id)})
            request.session.update({"token": access_token})

        return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")

        if not token:
            return False

        user = await get_current_user(token=token)
        if not user:
            return False

        return True


authentication_backend = AdminAuth(secret_key=settings.SECRET_KEY)
