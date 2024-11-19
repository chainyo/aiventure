"""Authentication routes."""

from datetime import timedelta
from typing import AsyncGenerator

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi import status as http_status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from aiventure.config import settings
from aiventure.db import UsersCRUD
from aiventure.dependencies import get_async_session
from aiventure.models import StatusMessage, Token, TokenData, UserCreate, UserRead
from aiventure.utils import create_access_token


credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/authenticate")
router = APIRouter()


async def get_users_crud(session: AsyncSession = Depends(get_async_session)) -> AsyncGenerator[UsersCRUD, None]:
    """Get the users crud."""
    async with UsersCRUD(session) as crud:
        yield crud


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    users_crud: UsersCRUD = Depends(get_users_crud),
) -> UserRead | None:
    """Get current user"""
    try:
        payload = jwt.decode(token, settings.openssl_key, algorithms=[settings.algorithm])
        username: str = payload.get("sub")

        if username is None:
            raise credentials_exception

        token_data = TokenData(username=username)

    except JWTError as e:
        raise credentials_exception from e

    user = await users_crud.get_by_email(token_data.username)

    if user is None:
        raise credentials_exception

    return UserRead.model_validate(user)


@router.post("/create", response_model=UserRead | None, status_code=http_status.HTTP_201_CREATED)
async def create_user(data: UserCreate, users: UsersCRUD = Depends(get_users_crud)) -> UserRead | None:
    """Create a new user"""
    if await users.get_by_email(data.email):
        return None

    user = await users.create(data)

    return UserRead.model_validate(user)


@router.get("/me", response_model=UserRead | None, status_code=http_status.HTTP_200_OK)
async def get_current_user_info(current_user: UserRead = Depends(get_current_user)) -> UserRead | None:
    """Get the current user"""
    return current_user


@router.post(
    "/authenticate",
    response_model=Token,
    status_code=http_status.HTTP_200_OK,
    responses={
        200: {"model": Token},
        401: {"model": StatusMessage},
    },
)
async def authenticate_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    users: UsersCRUD = Depends(get_users_crud),
) -> JSONResponse:
    """Authenticate a user"""
    user = await users.authenticate(form_data.username, form_data.password)

    match user:
        case None:
            return JSONResponse(
                status_code=http_status.HTTP_401_UNAUTHORIZED,
                content={"status": False, "message": "Incorrect username or password"},
            )
        case _:
            pass

    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(data={"sub": user.email}, expires_delta=access_token_expires)

    return JSONResponse(
        status_code=http_status.HTTP_200_OK, content={"access_token": access_token, "token_type": "bearer"}
    )


@router.get("/refresh", response_model=Token, status_code=http_status.HTTP_200_OK)
async def refresh_user_token(current_user: UserRead = Depends(get_current_user)) -> JSONResponse:
    """Refresh a user's token"""
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(data={"sub": current_user.email}, expires_delta=access_token_expires)

    return JSONResponse(
        status_code=http_status.HTTP_200_OK, content={"access_token": access_token, "token_type": "bearer"}
    )


@router.delete(
    "/{email}",
    response_model=StatusMessage,
    responses={
        200: {"model": StatusMessage},
        404: {"model": StatusMessage},
    },
)
async def delete_user(
    current_user: UserRead = Depends(get_current_user),
    users: UsersCRUD = Depends(get_users_crud),
) -> JSONResponse:
    """Delete a user"""
    status = await users.delete(current_user.email)

    match status:
        case False:
            _status_code = http_status.HTTP_404_NOT_FOUND
            _message = "The user does not exist!"
        case True:
            _status_code = http_status.HTTP_200_OK
            _message = "The user has been deleted!"
    return JSONResponse(
        status_code=_status_code,
        content={"status": status, "message": _message},
    )
