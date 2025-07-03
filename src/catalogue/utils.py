from typing import Annotated

from elasticsearch import AsyncElasticsearch
from elasticsearch.dsl import Index, Search, AsyncIndex
from fastapi import Depends

from src.catalogue.models.elasticsearch import PRODUCT_INDEX, ProductIndex
from src.catalogue.models.pydantic import ProductElasticResponse
from src.catalogue.models.sqlalchemy import Product
from src.common.databases.elasticsearch import elastic_client


class ProductElasticManager:
    def __init__(self, client: Annotated[AsyncElasticsearch, Depends(elastic_client)] = elastic_client):
        self.client = client

    async def init_indices(self):
        product_index = AsyncIndex(
            name=PRODUCT_INDEX,
            using=self.client,
        )

        product_index.document(ProductIndex)

        if not await product_index.exists():
            await product_index.create()

    @staticmethod
    def _build_product_search_query(keyword):
        search = Search(
            index=PRODUCT_INDEX
        ).query(
            'multi_match',
            query=keyword,
            fields=["title", "description", "short_description"]
        )
        return search.to_dict()
        # x = MultiMatch(query=keyword, fields=["title", "description", "short_description"])

    async def search_product(self, keyword):
        query = self._build_product_search_query(keyword)
        response = await self.client.search(index=PRODUCT_INDEX, body=query)
        await self.client.close()

        hits = response.get('hits', {}).get('hits', {})
        sorted_hits = sorted(hits, key=lambda x: x.get("_score", 0), reverse=True)

        sorted_response = [
            ProductElasticResponse(
                product_id=hit.get("_id", ''),
                title=hit.get("_source", {}).get("title"),
                score=hit.get("_score", {}),

            )
            for hit in sorted_hits
        ]
        return sorted_response

    async def update_index(self, products: list[Product]) -> None:
        bulk_data = []
        for product in products:
            action = {"index": {"_index": PRODUCT_INDEX, "_id": product.id}}
            data = {
                "title": product.title,
                "description": product.description,
                "short_description": product.short_description,
            }
            bulk_data.append(action)
            bulk_data.append(data)

            if len(bulk_data) >= 100:
                await self.client.bulk(body=bulk_data)
                bulk_data = []

        if bulk_data:
            await self.client.bulk(body=bulk_data)
