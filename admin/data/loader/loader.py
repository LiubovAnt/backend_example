import sqlite3
from dataclasses import asdict

from backoff import backoff
from psycopg2.extensions import connection as _connection

SELECT_LIMIT = 1000


class SQLiteLoader:
    @backoff
    def __init__(self, connection: sqlite3.Connection, table_classes):
        self.cursor = connection.cursor()
        self.limit = SELECT_LIMIT
        self.offset = 0
        self.table_classes = table_classes
        # чтение размера таблиц
        for table_class in self.table_classes:
            self._table_len(table_class)

    @backoff
    def load_movies(self, table_class):
        self.cursor.execute(table_class.select_query, (self.limit, self.offset))
        data = self.cursor.fetchall()
        # форматирование под dataclass
        format_data = [table_class(*row) for row in data]
        self.offset += self.limit
        if self.offset >= table_class.len:
            self.offset = 0
        return format_data

    # Чтение размера таблиц
    @backoff
    def _table_len(self, table_class):
        self.cursor.execute(table_class.len_query)
        length = self.cursor.fetchall()[0][0]
        table_class.len = length


class PostgresSaver:
    @backoff
    def __init__(
        self,
        pg_conn: _connection,
        table_classes,
        clean_table: bool = False,
    ):
        pg_conn.autocommit = True
        self.cursor = pg_conn.cursor()
        self.offset = 0
        self.limit = SELECT_LIMIT
        self.table_classes = table_classes
        # Отчишаем таблицы, если пришел флаг на отчистку
        if clean_table:
            for table_class in self.table_classes:
                self._clean_table(table_class)

    @backoff
    def save_all_data(self, data, table_class):
        data_dict = tuple([asdict(item) for item in data])
        self.cursor.executemany(table_class.insert_query, data_dict)

    @backoff
    # Отчистка таблиц
    def _clean_table(self, table_class):
        self.cursor.execute(table_class.clean_query)


def load_from_sqlite(
    connection: sqlite3.Connection,
    pg_conn: _connection,
    table_classes,
):
    # Основной метод загрузки данных из SQLite в Postgres
    sqlite_loader = SQLiteLoader(connection, table_classes)
    clean_table = True
    postgres_saver = PostgresSaver(pg_conn, table_classes, clean_table)
    # идем по таблицам
    for table_class in table_classes:
        # вызываем функцию достаточное колличество раз,
        # чтобы пройти по всей таблице, за индексами она сама следит
        for _ in range(0, table_class.len, SELECT_LIMIT):
            data = sqlite_loader.load_movies(table_class)
            postgres_saver.save_all_data(data, table_class)
