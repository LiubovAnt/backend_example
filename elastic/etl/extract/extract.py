import datetime
import logging
import uuid
from typing import List, Tuple, Type

from conf import LIMIT
from extract.db_date_classes import (
    EnricherData,
    FilmSQL,
    GenreSQL,
    PersonSQL,
    ProducterData,
)
from extract.db_extract import ExtractDB, db
from storage.state import State


class Producter:
    def __init__(self, data_base: ExtractDB, state_saver: State):
        self.db = data_base
        self.state_saver = state_saver
        self.limit = LIMIT
        self.state_dict = {}

    def get_first_date(self, table: str):
        # Загрузка последней перенесенной даты
        mod_data = self.state_saver.get_state(table)
        if mod_data:
            return datetime.datetime.strptime(mod_data, "%Y-%m-%d %H:%M:%S.%f%z")
        # Запрос старейшей записи
        query = self.db.query_with_prop(ProducterData.query_modified, {"table": table})
        ans = self.db.execute(query)
        if ans:
            return ans[0][0]

    def get_count_new(self, table: str, modified: datetime.datetime):
        # Подсчет колличества новых записей
        query = self.db.query_with_prop(ProducterData.query_count, {"table": table})
        ans = self.db.execute(query, (modified,))
        return ans[0][0]

    def get_data(self, table: str) -> Tuple[List, list[uuid.UUID]]:
        # Загрузка последней перенесенной даты
        modified = self.get_first_date(table)
        # Подсчет элементов в базе
        count = self.get_count_new(table, modified)
        offset = 0
        log_str = """
        [{datetime}]: Проверяем таблицу {table},
        Последнее перенесенное изменение {modified},
        Колличество новых = {count}
        """
        logging.info(
            log_str.format(
                datetime=datetime.datetime.now(),
                table=table,
                modified=modified,
                count=count,
            )
        )

        if table == "genre":
            data_class = GenreSQL
            query = data_class.query
        else:
            data_class = ProducterData
            query = self.db.query_with_prop(data_class.query, {"table": table})

        # Обращение к базе данных
        while offset < count:
            data = self.db.execute(query, (modified, offset, self.limit))
            format_data = [data_class(**row) for row in data]
            id_set = [row.id for row in format_data]
            # Меняем состояние
            offset += self.limit
            self.state_dict[table] = format_data[-1].modified
            yield format_data, id_set


class Enricher:
    def __init__(self, data_base: ExtractDB):
        self.db = data_base
        self.limit = LIMIT

    def get_ids(
        self,
        table: str,
        query_id_set: list[uuid.UUID],
    ) -> list[uuid.UUID]:
        offset = 0

        if table == "film_work":
            # Смотрим каких людей обновлять (могут измениться роли)
            query_count = self.db.query_with_prop(
                EnricherData.query_count_fw, {"table": "person_film_work"}
            )
            query_data = EnricherData.query_fw
        else:
            prop = {
                "table": "{table}_film_work".format(table=table),
                "id": "{table}_id".format(table=table),
            }
            # Если изменились person или ganre - cмотрим какие фильмы обновлять
            query_count = self.db.query_with_prop(EnricherData.query_count, prop)
            query_data = self.db.query_with_prop(EnricherData.query, prop)

        count = self.db.execute(query_count, (tuple(query_id_set),))[0][0]

        while offset < count:
            data = self.db.execute(
                query_data, (tuple(query_id_set), offset, self.limit)
            )
            offset += self.limit
            i = 0
            while i < (len(data)):
                if data[i][0] is None:
                    data.pop(i)
                else:
                    i += 1
            format_data = [EnricherData(**row) for row in data]
            id_set = [row.id for row in format_data]
            yield id_set

    def get_id_set(self, table: str, producer_id_set):
        # Собираем id set, чтобы избежать повторов в данных
        id_set = set()
        for ids in self.get_ids(table, producer_id_set):
            id_set = id_set.union(set(ids))
        return id_set


class Merger:
    def __init__(self, data_base: ExtractDB):
        self.db = data_base
        self.limit = LIMIT

    def get_data(self, id_set: list[uuid.UUID], data_class: Type) -> List:
        # Выбераем данные film_work, которые будем обновлять
        # Колличество id должно быть ограничено
        query = data_class.query
        data = self.db.execute(query, (tuple(id_set),))
        return [data_class(**row) for row in data]

    def get_limit_data(
        self,
        id_list: list[uuid.UUID],
        data_class: Type,
    ) -> List:
        while id_list:
            if len(id_list) > self.limit:
                ids = id_list[: self.limit]
                id_list = id_list[self.limit :]
            else:
                ids = id_list
                id_list = []
            data = self.get_data(ids, data_class)
            yield data


class Extract:
    def __init__(self, dsl: dict, state_saver: State):
        # Поднятие соединения
        self.db = db(dsl)
        self.producter = Producter(self.db, state_saver)
        self.enricher = Enricher(self.db)
        self.merger = Merger(self.db)

    def genres(self):
        table = "genre"
        for data, id_set in self.producter.get_data(table):
            film_id_set = self.enricher.get_id_set(table, id_set)
            yield data, film_id_set

    def person(self):
        table = "person"
        for _, id_set in self.producter.get_data(table):
            data = self.merger.get_data(id_set, PersonSQL)
            film_id_set = self.enricher.get_id_set(table, id_set)
            yield data, film_id_set

    def film(self, film_id_set=None):
        if not film_id_set:
            film_id_set = set()
        table = "film_work"
        # собираем film_work_ids и связанные person_ids
        person_ids_set = set()
        for _, producer_id_set in self.producter.get_data(table):
            ids_set = self.enricher.get_id_set(table, producer_id_set)
            film_id_set = film_id_set.union(set(producer_id_set))
            person_ids_set = person_ids_set.union(set(ids_set))
        # Выгружаем данные по фильмам
        film_id_list = list(film_id_set)
        yield from self.merger.get_limit_data(film_id_list, FilmSQL)
        # Выгружаем данные по персонам, которым могли добавиться фильмы
        person_ids_list = list(person_ids_set)
        yield from self.merger.get_limit_data(person_ids_list, PersonSQL)

    def get_data(self):
        film_id_set = set()
        for genre_data, genre_film_ids in self.genres():
            yield genre_data
            film_id_set = film_id_set.union(genre_film_ids)
        for person_data, person_film_ids in self.person():
            yield person_data
            film_id_set = film_id_set.union(person_film_ids)
        yield from self.film(film_id_set)
