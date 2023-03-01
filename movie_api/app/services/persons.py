from functools import lru_cache

from aioredis import Redis
from db.elastic import get_elastic
from db.redis import get_redis
from elasticsearch import AsyncElasticsearch
from fastapi import Depends
from models.persons import Person
from services.base import AbstractBaseService, BaseService


class PersonService(AbstractBaseService):
    pass


class PersonService(BaseService, PersonService):
    def __init__(self, caсhe_storage, db_storage):
        super().__init__(caсhe_storage, db_storage)
        self.table = "persons"
        self.data_class = Person
        self.search_fields = ["full_name"]


@lru_cache()
def get_person_service(
    caсhe_storage: Redis = Depends(get_redis),
    db_storage: AsyncElasticsearch = Depends(get_elastic),
) -> PersonService:
    return PersonService(caсhe_storage, db_storage)
