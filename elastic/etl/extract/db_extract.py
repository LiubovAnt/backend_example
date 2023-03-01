from abc import ABC, abstractmethod

from backoff import backoff
from psycopg2 import connect, extras, sql


class ExtractDB(ABC):
    @abstractmethod
    def __init__(self, dsl: dict):
        pass

    @abstractmethod
    def execute(self, query, data):
        pass

    @abstractmethod
    def query_with_prop(self, query: str, prop: dict):
        pass

    @abstractmethod
    def close(self):
        pass


class PostgresDB(ExtractDB):
    @backoff
    def __init__(self, dsl: dict):
        # Поднимаем соединение
        self.cursor = connect(**dsl, cursor_factory=extras.DictCursor).cursor()

    @backoff
    def execute(self, query: sql.Composed or str, data=None):
        # Загружаем данные
        if data:
            self.cursor.execute(query, data)
        else:
            self.cursor.execute(query)
        return self.cursor.fetchall()

    def query_with_prop(self, query: str, prop: dict):
        # Добавление переменных в запрос
        prop = {key: sql.Identifier(prop[key]) for key in prop}
        return sql.SQL(query).format(**prop)

    def close(self):
        # закрываем соединение
        self.cursor.close()


extras.register_uuid()
db = PostgresDB
