from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_password_hash, verify_password
from app.models.db_models import User


class UserAlreadyExistsError(Exception):
    """用户名已存在"""


class InvalidCredentialsError(Exception):
    """用户名或密码错误"""


class UserService:
    async def create_user(self, session: AsyncSession, username: str, password: str) -> User:
        existing = await session.execute(select(User).where(User.username == username))
        if existing.scalar_one_or_none():
            raise UserAlreadyExistsError("用户名已存在")

        user = User(username=username, hashed_password=get_password_hash(password))
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user

    async def authenticate(self, session: AsyncSession, username: str, password: str) -> User:
        result = await session.execute(select(User).where(User.username == username))
        user = result.scalar_one_or_none()
        if not user or not verify_password(password, user.hashed_password):
            raise InvalidCredentialsError("用户名或密码错误")
        return user


user_service = UserService()


