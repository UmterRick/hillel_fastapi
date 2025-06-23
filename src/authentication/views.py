from typing import Annotated

from asyncpg.pgproto.pgproto import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from src.authentication import security
from src.authentication.models import Token
from src.base_settings import base_settings
from src.users.services import get_user_service

router = APIRouter()

@router.post("/token", response_model=Token)
async def get_token(
    service: Annotated[get_user_service, Depends()],
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> dict:
    user = await service.authenticate(email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email or password")

    access_token_expires = timedelta(minutes=base_settings.auth.access_token_expire_minutes)

    return {
        "access_token": security.create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer"
    }
