from typing import Any

from extract.db_date_classes import FilmSQL, GenreSQL, PersonSQL
from load.es_date_classes import FilmES, GenreES, PersonES


class Transform:
    def run(self, extract_data: list) -> list:
        if isinstance(extract_data[0], GenreSQL):
            return self.run_genre(extract_data)
        elif isinstance(extract_data[0], PersonSQL):
            return self.run_person(extract_data)
        elif isinstance(extract_data[0], FilmSQL):
            return self.run_film(extract_data)

    def run_genre(self, extract_data: list):
        transform_data = []
        for row in extract_data:
            doc = {
                "uuid": str(row.id),
                "name": row.name,
                "description": row.description,
            }
            transform_data.append(GenreES(**doc))
        return transform_data

    def run_person(self, extract_data):
        data = {}
        for row in extract_data:
            # Если персоны с таким id не существует data
            # создаем элемент item для агрегации данных
            if row.id not in data:
                item = {
                    "role": set(),
                    "film_ids": set(),
                }
            if row.role:
                item["role"].add(row.role)
            if row.film_ids:
                item["film_ids"].add(str(row.film_ids))
            # Теперь данные с вычещенными повторами
            #  преобразуем под схему документа
            doc = {
                "uuid": str(row.id),
                "full_name": row.full_name,
                "role": self._check_na(list(item["role"])),
                "film_ids": self._check_na(list(item["film_ids"])),
            }
            data[row.id] = PersonES(**doc)
        return list(data.values())

    def run_film(self, extract_data):
        data = {}
        for row in extract_data:
            # Если фильма с таким id не существует data
            # создаем элемент item для агрегации данных
            if row.id not in data:
                item = {
                    "genre": {},
                    "director": {},
                    "actor": {},
                    "writer": {},
                }
            # С помощью item гарантируем отсутствие повторений
            if row.genre:
                item["genre"][str(row.genre_id)] = row.genre
            if row.role:
                item[row.role][str(row.person_id)] = row.full_name
            # Теперь данные с вычещенными повторами
            # преобразуем под схему документа
            doc = {
                "uuid": str(row.id),
                "title": row.title,
                "imdb_rating": row.imdb_rating,
                "description": row.description,
                "genre_names": self._get_val(item["genre"]),
                "directors_names": self._get_val(item["director"]),
                "actors_names": self._get_val(item["actor"]),
                "writers_names": self._get_val(item["writer"]),
                "genre": self._get_list_dict(item["genre"], val_name="name"),
                "actors": self._get_list_dict(item["actor"]),
                "writers": self._get_list_dict(item["writer"]),
                "directors": self._get_list_dict(item["director"]),
            }
            data[row.id] = FilmES(**doc)
        return list(data.values())

    def _get_val(self, val_dict):
        return self._check_na(list(val_dict.values()))

    def _get_list_dict(self, val_dict, val_name="full_name"):
        ans = [{"uuid": str(key), val_name: val} for key, val in val_dict.items()]
        return self._check_na(ans)

    def _check_na(self, item: Any):
        # Чистим пустые коллекции
        if not item:
            return None
        return item
