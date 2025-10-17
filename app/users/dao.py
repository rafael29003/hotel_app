from sqlalchemy import select

from app.dao.base import BaseDao
from app.database import async_session_maker
from app.users.models import Users


class UsersDAO(BaseDao):
    model = Users
