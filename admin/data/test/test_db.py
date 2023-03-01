import datetime
import os
import sqlite3
from typing import ClassVar

import psycopg2
import pytest
from psycopg2.extras import DictCursor

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")

POSTGRES_BD = {
    "dbname": DB_NAME,
    "user": DB_USER,
    "password": DB_PASSWORD,
    "host": DB_HOST,
    "port": 5432,
}

LITE_BD = "./db.sqlite"


class Genre:
    table_name: ClassVar[str] = "genre"
    lite_len_query: ClassVar[str] = "SELECT COUNT(*) FROM genre"
    lite_select_query: ClassVar[str] = "".join(
        ["SELECT name, description, ", "created_at, updated_at, id ", "FROM genre"]
    )
    post_len_query: ClassVar[str] = "SELECT COUNT(*) FROM content.genre"
    post_select_query: ClassVar[str] = "".join(
        ["SELECT name, description, ", "created, modified, id ", "FROM content.genre"]
    )


class FilmWork:
    table_name: ClassVar[str] = "film_work"
    lite_len_query: ClassVar[str] = "SELECT COUNT(*) FROM film_work"
    lite_select_query: ClassVar[str] = "".join(
        [
            "SELECT title, description, ",
            "certificate, file_path, rating, type, ",
            "created_at, updated_at, id ",
            "FROM film_work",
        ]
    )
    post_len_query: ClassVar[str] = "SELECT COUNT(*) FROM content.film_work"
    post_select_query: ClassVar[str] = "".join(
        [
            "SELECT title, description, ",
            "certificate, file_path, rating, type, ",
            "created, modified, id ",
            "FROM content.film_work",
        ]
    )


class Person:
    table_name: ClassVar[str] = "person"
    lite_len_query: ClassVar[str] = "SELECT COUNT(*) FROM person"
    lite_select_query: ClassVar[str] = "".join(
        ["SELECT full_name, ", "birth_date, created_at, updated_at, id ", "FROM person"]
    )
    post_len_query: ClassVar[str] = "SELECT COUNT(*) FROM content.person"
    post_select_query: ClassVar[str] = "".join(
        [
            "SELECT full_name,",
            "birth_date, created, modified, id ",
            "FROM content.person",
        ]
    )


class GenreFilmWork:
    table_name: ClassVar[str] = "genre_film_work"
    lite_len_query: ClassVar[str] = "SELECT COUNT(*) FROM genre_film_work"
    lite_select_query: ClassVar[str] = "".join(
        ["SELECT film_work_id, genre_id, ", "created_at, id ", "FROM genre_film_work"]
    )
    post_len_query: ClassVar[str] = "".join(
        ["SELECT COUNT(*) ", "FROM content.genre_film_work"]
    )
    post_select_query: ClassVar[str] = "".join(
        [
            "SELECT film_work_id, genre_id, ",
            "created, id ",
            "FROM content.genre_film_work",
        ]
    )


class PersonFilmWork:
    table_name: ClassVar[str] = "person_film_work"
    lite_len_query: ClassVar[str] = "".join(
        ["SELECT COUNT(*) ", "FROM person_film_work"]
    )
    lite_select_query: ClassVar[str] = "".join(
        [
            "SELECT film_work_id, person_id, ",
            "role, created_at, id ",
            "FROM person_film_work",
        ]
    )
    post_len_query: ClassVar[str] = "".join(
        ["SELECT COUNT(*) ", "FROM content.person_film_work"]
    )
    post_select_query: ClassVar[str] = "".join(
        [
            "SELECT film_work_id, ",
            "person_id, role, created, id ",
            "FROM content.person_film_work",
        ]
    )


@pytest.mark.parametrize(
    "table_class", [Genre, FilmWork, Person, GenreFilmWork, PersonFilmWork]
)
def test_length(table_class):
    # Проверяем длины таблиц
    with sqlite3.connect(LITE_BD) as sqlite_conn:
        with psycopg2.connect(
            **POSTGRES_BD,
            cursor_factory=DictCursor,
        ) as pg_conn:
            lite_cursor = sqlite_conn.cursor()
            lite_cursor.execute(table_class.lite_len_query)
            lite_len = lite_cursor.fetchall()[0][0]
            post_cursor = pg_conn.cursor()
            post_cursor.execute(table_class.post_len_query)
            post_len = post_cursor.fetchall()[0][0]
    assert lite_len == post_len


@pytest.mark.parametrize(
    "table_class",
    [Genre, FilmWork, Person, GenreFilmWork, PersonFilmWork],
)
def test_content(table_class):
    # Проверяем контент
    with sqlite3.connect(LITE_BD) as sqlite_conn:
        # sqlite
        lite_cursor = sqlite_conn.cursor()
        lite_cursor.execute(table_class.lite_select_query)
        lite_data = lite_cursor.fetchall()
        # собираем словарь с id в качестве ключа
        lite_dict = {}
        for item in lite_data:
            key = item[-1]
            val = []
            # Переводим в числовой формат
            for i in item[:-1]:
                try:
                    i = datetime.datetime.strptime(
                        "{time}:00".format(time=i), "%Y-%m-%d %H:%M:%S.%f%z"
                    )
                except ValueError:
                    pass
                except TypeError:
                    pass
                val.append(i)
            lite_dict[key] = val
    with psycopg2.connect(**POSTGRES_BD, cursor_factory=DictCursor) as pg_conn:
        # postgres
        post_cursor = pg_conn.cursor()
        post_cursor.execute(table_class.post_select_query)
        post_data = post_cursor.fetchall()
        post_dict = {vals[-1]: list(vals[:-1]) for vals in post_data}
    assert lite_dict == post_dict
