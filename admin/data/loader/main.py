import os
import sqlite3

import psycopg2
from loader import load_from_sqlite
from psycopg2.extras import DictCursor
from tables import FilmWork, Genre, GenreFilmWork, Person, PersonFilmWork

if __name__ == "__main__":
    # параметры для PostgreSQL
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    dsl = {
        "dbname": DB_NAME,
        "user": DB_USER,
        "password": DB_PASSWORD,
        "host": DB_HOST,
        "port": 5432,
    }

    sqlite_conn = sqlite3.connect("./db.sqlite")
    pg_conn = psycopg2.connect(**dsl, cursor_factory=DictCursor)

    table_classes = [Genre, FilmWork, Person, GenreFilmWork, PersonFilmWork]
    load_from_sqlite(sqlite_conn, pg_conn, table_classes)

    sqlite_conn.close()
    pg_conn.close()
