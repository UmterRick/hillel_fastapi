from elasticsearch import AsyncElasticsearch

from src.base_settings import base_settings

elastic_client = AsyncElasticsearch(hosts=base_settings.elasticsearch.hosts)