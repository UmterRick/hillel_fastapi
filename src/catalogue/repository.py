from fastapi import Depends
from src.catalogue.models.pydantic import ProductModel
from src.catalogue.models.sqlalchemy import Product
from src.common.databases.postgres import get_session
from src.common.repository.sqlalchemy import BaseSqlAlchemyRepository
from src.catalogue.models.sqlalchemy import StockRecord
from src.catalogue.models.pydantic import StockRecordModel
from sqlalchemy import select


from sqlalchemy.ext.asyncio import AsyncSession

class ProductRepository(BaseSqlAlchemyRepository[Product, ProductModel]):
    def __init__(self, session: AsyncSession):
        super().__init__(model=Product, pydantic_model=ProductModel, session=session)



def get_product_repository(session: AsyncSession = Depends(get_session)) -> ProductRepository:
    return ProductRepository(session=session)



class StockRecordRepository(BaseSqlAlchemyRepository[StockRecord, StockRecordModel]):
    def __init__(self, session: AsyncSession):
        super().__init__(model=StockRecord, pydantic_model=StockRecordModel, session=session)


    async def get_latest_by_product_id(self, product_id: int) -> StockRecord:
        stmt = (
            select(self.model)
            .where(self.model.product_id == product_id)
            .order_by(self.model.date_created.desc())
            .limit(1)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()


def get_stock_record_repository(session: AsyncSession = Depends(get_session)) -> StockRecordRepository:
    return StockRecordRepository(session=session)