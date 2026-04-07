from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api.deps import get_auth_service, get_current_active_user
from app.db.models.user import User
from app.schemas.auth import Token, UserRegister
from app.schemas.user import UserRead
from app.services.auth_service import AuthService

router = APIRouter()


AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]
CurrentUserDep = Annotated[User, Depends(get_current_active_user)]


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(payload: UserRegister, service: AuthServiceDep) -> UserRead:
    return service.register_user(payload)


@router.post("/login", response_model=Token)
def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: AuthServiceDep,
) -> Token:
    access_token = service.authenticate_user(form_data.username, form_data.password)
    return Token(access_token=access_token)


@router.get("/me", response_model=UserRead)
def me(current_user: CurrentUserDep) -> UserRead:
    return current_user
