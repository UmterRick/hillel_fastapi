from fastapi import Depends
from src.orders.models.pydantic import BasketLineModel, BasketModel, OrderLineModel, OrderModel
from src.orders.models.sqlalchemy import BasketLine, Basket, OrderLine, Order
from src.common.databases.postgres import get_session
from src.common.repository.sqlalchemy import BaseSqlAlchemyRepository

from sqlalchemy.ext.asyncio import AsyncSession



class BasketLineRepository(BaseSqlAlchemyRepository[BasketLine, BasketLineModel]):
    def __init__(self, session: AsyncSession):
        super().__init__(model=BasketLine, pydantic_model=BasketLineModel, session=session)


def get_basket_line_repository(session: AsyncSession = Depends(get_session)) -> BasketLineRepository:
    return BasketLineRepository(session=session)



class BasketRepository(BaseSqlAlchemyRepository[Basket, BasketModel]):
    def __init__(self, session: AsyncSession):
        super().__init__(model=Basket, pydantic_model=BasketModel, session=session)


def get_basket_repository(session: AsyncSession = Depends(get_session)) -> BasketRepository:
    return BasketRepository(session=session)



class OrderLineRepository(BaseSqlAlchemyRepository[OrderLine, OrderLineModel]):
    def __init__(self, session: AsyncSession):
        super().__init__(model=OrderLine, pydantic_model=OrderLineModel, session=session)


def get_order_line_repository(session: AsyncSession = Depends(get_session)) -> OrderLineRepository:
    return OrderLineRepository(session=session)



class OrderRepository(BaseSqlAlchemyRepository[Order, OrderModel]):
    def __init__(self, session: AsyncSession):
        super().__init__(model=Order, pydantic_model=OrderModel, session=session)


def get_order_repository(session: AsyncSession = Depends(get_session)) -> OrderRepository:
    return OrderRepository(session=session)

