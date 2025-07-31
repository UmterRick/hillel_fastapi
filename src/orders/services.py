from fastapi import Depends
from decimal import Decimal
from sqlalchemy import select

from src.orders.models.pydantic import (
    BasketLineModel,
    BasketModel,
    OrderLineModel,
    OrderModel,
    OrderCreateFromBasket,
    OrderUpdate,
)

from src.orders.repository import (
    BasketLineRepository, get_basket_line_repository,
    BasketRepository, get_basket_repository,
    OrderLineRepository, get_order_line_repository,
    OrderRepository, get_order_repository
)

from src.common.service import BaseService
from src.common.exceptions.base import ObjectDoesNotExistException

from src.catalogue.repository import (
    ProductRepository,
    get_product_repository,
    StockRecordRepository,
    get_stock_record_repository,
)

from src.users.models.sqlalchemy import UserAddress

from src.orders.models.sqlalchemy import Order, OrderLine



class BasketLineService(BaseService[BasketLineModel]):
    def __init__(
            self,
            repository: BasketLineRepository,
            product_repo: ProductRepository,
            stock_repo:StockRecordRepository,
            basket_repo: BasketRepository
    ):
        super().__init__(repository)
        self.product_repo = product_repo
        self.stock_repo = stock_repo
        self.basket_repo = basket_repo


    async def create(self, basket_line_data: BasketLineModel) -> BasketLineModel:
        product_id = basket_line_data.product_id
        quantity = basket_line_data.quantity
        product = await self.product_repo.get(product_id)
        stock_record = await self.stock_repo.get_latest_by_product_id(product_id)
        price = stock_record.price
        total_price = price * quantity
        basket_line_data.price = total_price

        basket_line = await super().create(basket_line_data)
        await self.update_basket_price(basket_line.basket_id)
        return basket_line


    async def update(self, basket_line_id: int, update_data: BasketLineModel) -> BasketLineModel:
        basket_line = await self.repository.get(basket_line_id)
        basket_line.quantity = update_data.quantity
        basket_line.product_id = update_data.product_id
        stock_record = await self.stock_repo.get_latest_by_product_id(update_data.product_id)
        basket_line.price = update_data.quantity * stock_record.price

        updated = await self.repository.update(basket_line_id, basket_line)
        await self.update_basket_price(updated.basket_id)
        return updated


    async def delete(self, basket_line_id: int):
        basket_line = await self.repository.get(basket_line_id)
        await self.repository.delete(basket_line_id)
        await self.update_basket_price(basket_line.basket_id)
        return basket_line


    async def update_basket_price(self, basket_id: int):
        basket_lines = await self.repository.filter(basket_id=basket_id)
        total_price = sum([line.price for line in basket_lines])
        basket = await self.basket_repo.get(basket_id)
        basket.price = total_price
        await self.basket_repo.update(basket_id, basket)


def get_basket_line_service(
        repo: BasketLineRepository = Depends(get_basket_line_repository),
        product_repo: ProductRepository = Depends(get_product_repository),
        stock_repo: StockRecordRepository = Depends(get_stock_record_repository),
        basket_repo: BasketRepository = Depends(get_basket_repository),
) -> BasketLineService:
    return BasketLineService(repo, product_repo, stock_repo, basket_repo)


class BasketService(BaseService[BasketModel]):
    def __init__(self, repository: BasketRepository):
        super().__init__(repository)


def get_basket_service(repo: BasketRepository = Depends(get_basket_repository)) -> BasketService:
    return BasketService(repository=repo)



class OrderLineService(BaseService[OrderLineModel]):
    def __init__(self, repository: OrderLineRepository):
        super().__init__(repository)


# services.py

# ❗️OrderLines are created automatically in OrderService.create_from_basket()
# Do NOT create/update/delete OrderLine manually.


def get_order_line_service(repo: OrderLineRepository = Depends(get_order_line_repository)) -> OrderLineService:
    return OrderLineService(repository=repo)



class OrderService(BaseService[OrderModel]):
    def __init__(self, repository: OrderRepository, basket_repo: BasketRepository, basket_line_repo: BasketLineRepository):
        super().__init__(repository)
        self.basket_repo = basket_repo
        self.basket_line_repo = basket_line_repo


    async def create_from_basket(self, order_data: OrderCreateFromBasket) -> OrderModel:
        basket = await self.basket_repo.get(order_data.basket_id)
        if not basket:
            raise ObjectDoesNotExistException("Basket not found")
        basket_lines = await self.basket_line_repo.filter(basket_id=order_data.basket_id)
        if not basket_lines:
            raise ObjectDoesNotExistException("Basket is empty")

        user_id = order_data.user_id
        address_id = order_data.address_id
        total_price = basket.price
        additional_info = order_data.additional_info
        status = order_data.status
        orders = (await self.repository.session.scalars(select(Order))).all()
        max_number = max((order.number or 0 for order in orders), default=10000)
        new_number = max_number + 1
        new_order = Order(
            number=new_number,
            user_id=user_id,
            basket_id=basket.id,
            address_id=address_id,
            total_price=total_price,
            shipping_price=Decimal("100.00"),
            shipping_method="Укрпошта",
            status=status,
            additional_info=order_data.additional_info
            )
        session = self.repository.session
        session.add(new_order)
        await session.flush()
        order_id = new_order.id
        # order_lines = []
        order_lines = [
            OrderLine(
                product_id=line.product_id,
                order_id=new_order.id,
                quantity=line.quantity,
                price=line.price,
            )
            for line in basket_lines
        ]
        session.add_all(order_lines)
        await session.commit()
        await session.refresh(new_order)
        return OrderModel.model_validate(new_order, from_attributes=True)


    async def list(self) -> list[OrderModel]:
        stmt = select(Order)  # selectinload більше не потрібен
        result = await self.repository.session.execute(stmt)
        orders = result.scalars().all()
        for order in orders:
            await self.repository.session.refresh(order)
        return [OrderModel.model_validate(o, from_attributes=True) for o in orders]


    async def detail(self, pk: int) -> OrderModel:
        stmt = select(Order).where(Order.id == pk)  # прибрав selectinload
        result = await self.repository.session.execute(stmt)
        order = result.scalar_one_or_none()
        if not order:
            raise ObjectDoesNotExistException()

        await self.repository.session.refresh(order)  # гарантовано заповнює всі поля
        return OrderModel.model_validate(order, from_attributes=True)


    async def update_order(self, order_id: int, update_data: OrderUpdate) -> OrderModel:
        stmt = select(Order).where(Order.id == order_id)
        result = await self.repository.session.execute(stmt)
        order = result.scalar_one_or_none()
        if not order:
            raise ObjectDoesNotExistException()
        update_dict = update_data.model_dump(exclude_unset=True)
        updated_model = OrderModel.model_validate(order, from_attributes=True).model_copy(update=update_dict)
        updated = await self.repository.update(order_id, updated_model)
        return updated


def get_order_service(
        repo: OrderRepository = Depends(get_order_repository),
        basket_repo: BasketRepository = Depends(get_basket_repository),
        basket_line_repo: BasketLineRepository = Depends(get_basket_line_repository)
) -> OrderService:
    return OrderService(repository=repo, basket_repo=basket_repo, basket_line_repo=basket_line_repo)