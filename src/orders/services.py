from fastapi import Depends

from src.orders.models.pydantic import BasketLineModel, BasketModel, OrderLineModel, OrderModel
from src.orders.repository import (
    BasketLineRepository, get_basket_line_repository,
    BasketRepository, get_basket_repository,
    OrderLineRepository, get_order_line_repository,
    OrderRepository, get_order_repository
)
from src.common.service import BaseService


class BasketLineService(BaseService[BasketLineModel]):
    def __init__(self, repository: BasketLineRepository):
        super().__init__(repository)


def get_basket_line_service(repo: BasketLineRepository = Depends(get_basket_line_repository)) -> BasketLineService:
    return BasketLineService(repository=repo)



class BasketService(BaseService[BasketModel]):
    def __init__(self, repository: BasketRepository):
        super().__init__(repository)


def get_basket_service(repo: BasketRepository = Depends(get_basket_repository)) -> BasketService:
    return BasketService(repository=repo)



class OrderLineService(BaseService[OrderLineModel]):
    def __init__(self, repository: OrderLineRepository):
        super().__init__(repository)


def get_order_line_service(repo: OrderLineRepository = Depends(get_order_line_repository)) -> OrderLineService:
    return OrderLineService(repository=repo)



class OrderService(BaseService[OrderModel]):
    def __init__(self, repository: OrderRepository):
        super().__init__(repository)

    async def get_order_with_address(self, order_id: int) -> OrderModel:
        return await self.repository.get_order_with_address(order_id)


def get_order_service(repo: OrderRepository = Depends(get_order_repository)) -> OrderService:
    return OrderService(repository=repo)