from abc import ABC
from typing import TypeVar, Generic, Union
from pydantic import BaseModel

from src.common.repository.beanie import BaseMongoRepository
from src.common.repository.sqlalchemy import BaseSqlAlchemyRepository

T = TypeVar("T")
PType = TypeVar("PType", bound=BaseModel)

class BaseMixin(ABC):
    repository: BaseSqlAlchemyRepository[T, PType]

class ReadMixin(BaseMixin):
    async def list(self) -> list[PType]:
        return await self.repository.all()


    async def detail(self, pk: int) -> PType:
        return await self.repository.get(pk=pk)

class WriteMixin(BaseMixin):
    async def create(self, instance_data: PType) -> PType:
        return await self.repository.create(instance_data)

    async def update(self, pk: int, instance_data: PType) -> PType:
        return await self.repository.update(pk, instance_data)

    async def delete(self, pk: int, ):
        return await self.repository.delete(pk)


class BaseService(ReadMixin, WriteMixin, Generic[PType]):
    def __init__(self, repository: Union[BaseSqlAlchemyRepository[T, PType], BaseMongoRepository[T]]):
        self.repository = repository