import json
import logging
from dataclasses import asdict
from typing import List

from backoff import backoff
from elasticsearch import Elasticsearch, helpers
from elasticsearch.exceptions import RequestError
from load.es_date_classes import FilmES, GenreES, PersonES


class Load:
    # 1. загружать данные пачками;
    # 2. без потерь переживать падение Elasticsearch;
    # 3. принимать/формировать поле, которое будет считаться id в Elasticsearch

    def __init__(self, es_adres: str):
        self.es_rise_connection(es_adres)

    @backoff
    def create_index(self, index: str, schema_file: str):
        try:
            with open(schema_file, "r") as f:
                schema = json.load(f)
            self.es_client.indices.create(
                index=index,
                body=schema,
            )
            logging.info("Индекс {index} был создан".format(index=index))
            self.refresh_storage = True
        except RequestError:
            logging.info("Индекс {index} уже существует".format(index=index))

    @backoff
    def es_rise_connection(self, es_adres):
        self.es_client = Elasticsearch(es_adres)
        # Флаг необходимости перезагрузки ETL c начала
        self.refresh_storage = False
        # Cоздаем 3 схемы, если их не существует
        # Фильмы
        self.create_index(index="movies", schema_file="load/films.json")
        # Жанры
        self.create_index(index="genres", schema_file="load/genres.json")
        # Персоны
        self.create_index(index="persons", schema_file="load/persons.json")

    @backoff
    def push_genres(self, data: List):
        actions = [
            {
                "_index": "genres",
                "_type": "_doc",
                "_id": doc.uuid,
                **asdict(doc),
            }
            for doc in data
        ]
        helpers.bulk(self.es_client, actions)

    @backoff
    def push_persons(self, data: List):
        actions = [
            {
                "_index": "persons",
                "_type": "_doc",
                "_id": doc.uuid,
                **asdict(doc),
            }
            for doc in data
        ]
        helpers.bulk(self.es_client, actions)

    @backoff
    def push_films(self, data: List):
        actions = [
            {
                "_index": "movies",
                "_type": "_doc",
                "_id": doc.uuid,
                **asdict(doc),
            }
            for doc in data
        ]
        helpers.bulk(self.es_client, actions)

    def push_data(self, data: List):
        if isinstance(data[0], GenreES):
            self.push_genres(data)
        elif isinstance(data[0], PersonES):
            self.push_persons(data)
        elif isinstance(data[0], FilmES):
            self.push_films(data)
