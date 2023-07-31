from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette import status

from app.api import deps
from app.core.security import (create_access_token, get_password_hash,
                               verify_password)
from app.schemas.users import UserSchema, UserSchemaAdd, UserTokenSchema
from app.services.users import UsersService

router = APIRouter()


@router.post("/add_user", response_model=UserTokenSchema)
async def add_user(
    user: UserSchemaAdd,
    users_service: UsersService = Depends(deps.users_service),
):
    existing_user = await users_service.get_user_by_login(user.login)
    if existing_user:
        raise HTTPException(
            status_code=401, detail="Такой пользователь уже зарегистрирован"
        )
    user.password = get_password_hash(user.password)
    created_user = await users_service.add_user(user)
    created_user = created_user.to_read_model()
    access_token = create_access_token(data=created_user.model_dump())
    return UserTokenSchema(access_token=access_token)


@router.post("/token", response_model=UserTokenSchema)
async def token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    users_service: UsersService = Depends(deps.users_service),
):
    user = await users_service.get_user_by_login(form_data.username)
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверное имя пользователя или пароль",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = user.to_read_model()
    access_token = create_access_token(data=user.model_dump())
    return UserTokenSchema(access_token=access_token)


@router.get("/info", response_model=UserSchema)
async def info(
    current_user: UserSchema = Depends(deps.get_current_user),
):
    return current_user
