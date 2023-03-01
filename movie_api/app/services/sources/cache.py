import abc
import json
from typing import Any, Callable, Optional

from aioredis import Redis

FILM_CACHE_EXPIRE_IN_SECONDS = 60 * 5  # минут


class AbstractStorage(abc.ABC):
    @abc.abstractmethod
    def __init__(self, **kwargs):
        pass

    # Операции с хранилищем
    @abc.abstractmethod
    async def from_cache(self, key: str) -> Optional[Any]:
        # Достаем данные из хранилища по id
        pass

    @abc.abstractmethod
    async def to_cache(self, key: str, item: Any):
        # Кладем данные в хранилище
        pass


class AbstractCache(abc.ABC):
    # Интерфейс взаимодействия
    @abc.abstractmethod
    def __init__(self, storage: AbstractStorage):
        pass

    @abc.abstractmethod
    async def make_caсhable(self, key: str, func: Callable) -> Optional[Any]:
        pass


class RedisStorage(AbstractStorage):
    def __init__(self, storage: Redis):
        self.redis = storage

    async def from_cache(self, key: str) -> Optional[Any]:
        # Пытаемся получить данные по id из кеша
        # (id для разных item уникальны, так что тип не важен)
        # https://redis.io/commands/get
        data = await self.redis.get(key)
        if not data:
            return None
        return json.loads(data.decode())

    async def to_cache(self, key: str, item):
        # Сохраняем данные о жанре, используя команду set
        # Выставляем время жизни кеша — 5 минут
        # https://redis.io/commands/set
        # pydantic позволяет сериализовать модель в json
        await self.redis.set(key, item, expire=FILM_CACHE_EXPIRE_IN_SECONDS)


class Cache(AbstractCache):
    def __init__(self, storage: AbstractStorage):
        self.storage = storage

    async def make_caсhable(self, key: str, func: Callable, data_class):
        # Пытаемся получить данные из кеша
        item = await self.storage.from_cache(key)
        # Не получается - обращаемся к основной bd
        if not item:
            item = await func
            if not item:
                return None
            # Если выдача не нулевая - кешируем
            if isinstance(item, list):
                data = [i.json() for i in item]
                await self.storage.to_cache(key, json.dumps(data))
            else:
                await self.storage.to_cache(key, item.json())
        elif isinstance(item, list):
            item = [data_class(**json.loads(i)) for i in item]
        else:
            item = data_class(**item)
        return item
