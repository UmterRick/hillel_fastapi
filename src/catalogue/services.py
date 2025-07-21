import datetime

from fastapi import Depends

from src.base_settings import base_settings
from src.catalogue.models.pydantic import ProductModel
from src.catalogue.repository import ProductRepository, get_product_repository
from src.catalogue.utils import ProductElasticManager
from src.common.enums import TaskStatus
from src.common.kafka_producer import producer
from src.common.service import BaseService
from elasticsearch.exceptions import ConnectionError

from src.general.schemas.task_status import TaskStatusModel


class ProductService(BaseService[ProductModel]):
    def __init__(self, repository: ProductRepository):
        super().__init__(repository)

    @staticmethod
    async def search(keyword: str):
        result = await ProductElasticManager().search_product(keyword=keyword)
        return result

    async def update_search_index(self, uuid):
        products = await self.list()

        try:
            await ProductElasticManager().update_index(products=products)
        except ConnectionError as exc:
            await TaskStatusModel(uuid=uuid, status=TaskStatus.ERROR, details=str(exc)).save_to_redis()

        await TaskStatusModel(
            uuid=uuid,
            status=TaskStatus.DONE,
            done_at=datetime.datetime.now(tz=datetime.timezone.utc).strftime(base_settings.date_time_format)
        ).save_to_redis()

    def _add_product_to_queue(self, instance_data):
        producer.send("product-topic", instance_data.model_dump_json().encode("utf-8"))

    async def create(self, instance_data):
        instance = await super().create(instance_data)
        self._add_product_to_queue(instance_data)
        return instance

def get_product_service(repo: ProductRepository = Depends(get_product_repository)) -> ProductService:
    return ProductService(repository=repo)