import abc
from functools import lru_cache
from typing import List, Optional

from aioredis import Redis
from db.elastic import get_elastic
from db.redis import get_redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends
from models.film import Film
from services.base import AbstractBaseService, BaseService


class AbstractFilmService(AbstractBaseService):
    @abc.abstractmethod
    async def sort(
        self,
        sort: str,
        number: int,
        size: int,
        genre=None,
    ) -> Optional[List[Film]]:
        pass


class FilmService(AbstractFilmService, BaseService):
    def __init__(self, caсhe_storage, db_storage):
        super().__init__(caсhe_storage, db_storage)
        self.table = "movies"
        self.data_class = Film
        self.search_fields = ["title", "description"]

    async def sort(
        self,
        sort: str,
        number: int,
        size: int,
        genre=None,
    ) -> Optional[List[Film]]:
        id = hash((genre, number, size))
        return await self.cache.make_caсhable(
            id,
            self.db.sort_film(
                table=self.table,
                sort=sort,
                number=number,
                size=size,
                genre=genre,
                data_class=self.data_class,
            ),
            self.data_class,
        )


@lru_cache()
def get_film_service(
    caсhe_storage: Redis = Depends(get_redis),
    db_storage: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(caсhe_storage, db_storage)
