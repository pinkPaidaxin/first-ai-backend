from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import create_access_token
from app.core.database import get_db
from app.models.schemas import AuthResponse, Response, UserCreate, UserInfo, UserLogin
from app.services.user_service import (
    InvalidCredentialsError,
    UserAlreadyExistsError,
    user_service,
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=Response[UserInfo])
async def register_user(payload: UserCreate, session: AsyncSession = Depends(get_db)):
    try:
        user = await user_service.create_user(
            session=session,
            username=payload.username,
            password=payload.password,
        )
    except UserAlreadyExistsError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )

    token = create_access_token(str(user.id))
    return Response(
        code=0,
        message="success",
        data=AuthResponse(
            user=UserInfo.model_validate(user),
            access_token=token,
        ),
    )


@router.post("/login", response_model=Response[UserInfo])
async def login_user(payload: UserLogin, session: AsyncSession = Depends(get_db)):
    try:
        user = await user_service.authenticate(
            session=session,
            username=payload.username,
            password=payload.password,
        )
    except InvalidCredentialsError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
        )

    token = create_access_token(str(user.id))
    return Response(
        code=0,
        message="success",
        data=AuthResponse(
            user=UserInfo.model_validate(user),
            access_token=token,
        ),
    )


