import abc
from functools import lru_cache
from typing import List, Optional

from aioredis import Redis
from db.elastic import get_elastic
from db.redis import get_redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends
from models.genre import Genre
from services.base import AbstractBaseService, BaseService


class AbstractFilmService(AbstractBaseService):
    @abc.abstractmethod
    async def get_list(self) -> Optional[List[Genre]]:
        pass


class GenreService(BaseService, AbstractFilmService):
    def __init__(self, caсhe_storages, db_storage):
        super().__init__(caсhe_storages, db_storage)
        self.table = "genres"
        self.data_class = Genre

    async def get_list(self) -> Optional[List[Genre]]:
        key = hash("genre")
        return await self.cache.make_caсhable(
            key,
            self.db.get_genres(table=self.table, data_class=self.data_class),
            self.data_class,
        )


@lru_cache()
def get_genre_service(
    caсhe_storages: Redis = Depends(get_redis),
    db_storage: AsyncElasticsearch = Depends(get_elastic),
) -> GenreService:
    return GenreService(caсhe_storages, db_storage)
