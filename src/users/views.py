from typing import Annotated, Union

from fastapi import APIRouter, Depends, status

from src.authentication.utils import get_current_user, get_current_active_user
from src.common.schemas.common import ErrorResponse
from src.users.models.pydantic import UserModel
from src.users.models.sqlalchemy import User

router = APIRouter()


@router.get("/",
             responses={
                 status.HTTP_200_OK: {'model': UserModel},
                 status.HTTP_404_NOT_FOUND: {'model': ErrorResponse}
             },
             response_model=UserModel)
async def user_detail(
        current_user: Annotated[UserModel, Depends(get_current_active_user)]
) -> UserModel |  ErrorResponse:
    return current_user
