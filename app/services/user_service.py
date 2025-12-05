from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_password_hash, verify_password
from app.models.db_models import User


class UserAlreadyExistsError(Exception):
    """邮箱已被注册"""


class InvalidCredentialsError(Exception):
    """邮箱或密码错误"""


class UserService:
    async def create_user(self, session: AsyncSession, username: str, email: str, password: str) -> User:
        # 检查邮箱是否已存在
        existing_email = await session.execute(select(User).where(User.email == email))
        if existing_email.scalar_one_or_none():
            raise UserAlreadyExistsError("邮箱已被注册")

        user = User(
            username=username,
            email=email,
            hashed_password=get_password_hash(password)
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user

    async def authenticate(self, session: AsyncSession, email: str, password: str) -> User:
        result = await session.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()
        if not user or not verify_password(password, user.hashed_password):
            raise InvalidCredentialsError("邮箱或密码错误")
        return user


user_service = UserService()


