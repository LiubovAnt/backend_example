import abc
from typing import Any, List, Optional

from aioredis import Redis
from elasticsearch import AsyncElasticsearch
from services.sources.cache import Cache, RedisStorage
from services.sources.db import ElasticLoader

FILM_CACHE_EXPIRE_IN_SECONDS = 60 * 5  # 5 минут


class AbstractBaseService(abc.ABC):
    @abc.abstractmethod
    def __init__(self, **kwargs):
        pass

    @abc.abstractmethod
    async def get_by_id(self, key: str) -> Optional[Any]:
        # Получение полной информации по ID
        pass

    @abc.abstractmethod
    async def get_by_ids(self, ids: List[str]) -> Optional[List]:
        # Получение списка по IDs
        pass

    @abc.abstractmethod
    async def search(
        self,
        query: str,
        number: int,
        size: int,
    ) -> Optional[List]:
        # Поиск по запросу
        pass


class BaseService(AbstractBaseService):
    def __init__(self, caсhe_storage: Redis, db_storage: AsyncElasticsearch):
        self.caсhe_storage = RedisStorage(caсhe_storage)
        self.cache = Cache(self.caсhe_storage)
        self.db = ElasticLoader(db_storage)
        self.table = None
        self.data_class = None
        self.search_fields = None

    async def get_by_id(self, id: str) -> Optional[List]:
        # Получение полной информации по ID
        return await self.cache.make_caсhable(
            id,
            self.db.get_by_id(table=self.table, id=id, data_class=self.data_class),
            self.data_class,
        )

    async def get_by_ids(self, ids: List[str]) -> Optional[List]:
        # Получение списка по IDs
        id = hash(tuple(ids))
        return await self.cache.make_caсhable(
            id,
            self.db.get_by_ids(table=self.table, ids=ids, data_class=self.data_class),
            self.data_class,
        )

    async def search(
        self,
        query: str,
        number: int,
        size: int,
    ) -> Optional[List]:
        # Поиск по запросу
        id = hash((query, number, size))
        return await self.cache.make_caсhable(
            id,
            self.db.search(
                table=self.table,
                query=query,
                number=number,
                size=size,
                search_fields=self.search_fields,
                data_class=self.data_class,
            ),
            self.data_class,
        )
