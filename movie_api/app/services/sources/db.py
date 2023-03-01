import abc
from typing import Any, List, Optional, Type

from elasticsearch import AsyncElasticsearch
from elasticsearch.exceptions import NotFoundError, RequestError
from services.sources.backoff import backoff


class AbstractLoader(abc.ABC):
    """В этом классе прописаны все обращения к базе данных."""

    # для всех таблиц
    @abc.abstractmethod
    async def get_by_id(
        self,
        table: str,
        key: str,
        data_class: Type,
    ) -> Optional[Any]:
        # Получить элемент по key
        pass

    @abc.abstractmethod
    async def search(
        self,
        table: str,
        query: str,
        number: int,
        size: int,
        search_fields: List[str],
        data_class: Type,
    ) -> Optional[List]:
        # Поиск элемента в таблице
        pass

    @abc.abstractmethod
    async def get_by_ids(
        self,
        table: str,
        ids: List,
        data_class: Type,
    ) -> Optional[List]:
        # Получить элементы по ids
        pass

    # специально для отдельных таблиц
    @abc.abstractmethod
    async def sort_film(
        self,
        table: str,
        sort: str,
        number: int,
        size: int,
        genre: Optional[str],
        data_class: Type,
    ) -> Optional[List]:
        # Сортировка фильмов
        pass

    @abc.abstractmethod
    async def get_genres(
        self,
        table: str,
        data_class: Type,
    ) -> Optional[List]:
        # Получить список жанров
        pass


class ElasticLoader(AbstractLoader):
    def __init__(self, elastic: AsyncElasticsearch):
        self.db = elastic

    # для всех таблиц
    @backoff
    async def get_by_id(
        self,
        table: str,
        id: str,
        data_class: Type,
    ) -> Optional[Any]:
        # Получить элемент по id
        try:
            doc = await self.db.get(table, id)
        except NotFoundError:
            return None
        return data_class(**doc["_source"])

    @backoff
    async def search(
        self,
        table: str,
        query: str,
        number: int,
        size: int,
        search_fields: List[str],
        data_class: Type,
    ) -> Optional[List]:
        # Поиск элемента в таблице
        try:
            body = {
                "size": size,
                "from": size * (number - 1),
                "query": {
                    "multi_match": {
                        "query": query,
                        "fields": search_fields,
                    },
                },
            }
            docs = await self.db.search(index=table, body=body)
            docs = docs["hits"]["hits"]
        except NotFoundError:
            return None
        ans = []
        for doc in docs:
            if "uuid" in doc["_source"]:
                ans.append(data_class(**doc["_source"]))
        return ans

    @backoff
    async def get_by_ids(
        self,
        table: str,
        ids: List,
        data_class: Type,
    ) -> Optional[List]:
        body = {
            "query": {
                "terms": {
                    "uuid": ids,
                },
            },
        }
        try:
            docs = await self.db.search(index=table, body=body)
            docs = docs["hits"]["hits"]
        except NotFoundError:
            return None
        ans = []
        for doc in docs:
            if "uuid" in doc["_source"]:
                ans.append(data_class(**doc["_source"]))
        return ans

    # специально для отдельных таблиц
    @backoff
    async def sort_film(
        self,
        table: str,
        sort: str,
        number: int,
        size: int,
        genre: Optional[str],
        data_class: Type,
    ) -> Optional[List]:
        # Сортировка фильмов
        order = "desc" if sort.startswith("-") else "asc"
        sort = sort.removeprefix("-")
        body = {
            "size": size,
            "from": size * (number - 1),
            "query": {
                "match_all": {},
            },
            "sort": [
                {
                    sort: {
                        "order": order,
                    },
                },
            ],
        }
        if genre:
            body["query"] = {
                "nested": {
                    "path": "genre",
                    "query": {
                        "bool": {
                            "must": {
                                "match": {
                                    "genre.uuid": genre,
                                },
                            },
                        },
                    },
                },
            }
        try:
            docs = await self.db.search(index=table, body=body)
            docs = docs["hits"]["hits"]
        except RequestError:
            return None
        ans = []
        for doc in docs:
            if "uuid" in doc["_source"]:
                ans.append(data_class(**doc["_source"]))
        return ans

    @backoff
    async def get_genres(self, table: str, data_class: Type) -> Optional[List]:
        # Получить список жанров
        body = {
            "query": {
                "match_all": {},
            },
        }
        try:
            docs = await self.db.search(index=table, body=body)
            docs = docs["hits"]["hits"]
        except NotFoundError:
            return None
        ans = []
        for doc in docs:
            if "uuid" in doc["_source"]:
                ans.append(data_class(**doc["_source"]))
        return ans
