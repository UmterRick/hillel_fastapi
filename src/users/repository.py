from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.databases.postgres import get_session
from src.common.repository.sqlalchemy import BaseSqlAlchemyRepository, PType
from src.users.models.pydantic import UserModel, UserWithPassword, UserAddressModel
from src.users.models.sqlalchemy import User, UserAddress


class UserRepository(BaseSqlAlchemyRepository[User, UserModel]):
    def __init__(self, session: AsyncSession):
        super().__init__(model=User, pydantic_model=UserModel, session=session)

    async def create(self, instance_data: PType) -> PType:
        raise NotImplementedError

    async def delete(self, pk: int):
        raise NotImplementedError

    async def get_by_email(self, email: str) -> UserWithPassword | None:
        stmt = select(self.model).where(self.model.email == email)
        result = await self.session.execute(stmt)
        user = result.scalar_one_or_none()
        if not user:
            return None
        return UserWithPassword.model_validate(user)


def get_user_repository(session: AsyncSession = Depends(get_session)) -> UserRepository:
    return UserRepository(session=session)


class UserAddressRepository(BaseSqlAlchemyRepository[UserAddress, UserAddressModel]):
    def __init__(self, session: AsyncSession):
        super().__init__(model=UserAddress, pydantic_model=UserAddressModel, session=session)


def get_user_address_repository(session: AsyncSession = Depends(get_session)) -> UserAddressRepository:
    return UserAddressRepository(session=session)