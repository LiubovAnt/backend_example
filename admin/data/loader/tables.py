import datetime
import uuid
from dataclasses import dataclass, field
from typing import ClassVar


@dataclass
class Genre:
    len: ClassVar[int] = 0
    len_query: ClassVar[str] = "SELECT COUNT(*) [int] FROM genre"
    select_query: ClassVar[str] = "".join(
        [
            "SELECT name [str], description [str], ",
            "created_at [datetime.datatime], ",
            "updated_at[datetime.datatime], id [uuid.UUID]",
            "FROM genre LIMIT ? OFFSET ?",
        ]
    )
    clean_query: ClassVar[str] = "TRUNCATE content.genre CASCADE"
    insert_query: ClassVar[str] = "".join(
        [
            "INSERT INTO content.genre ",
            "(id, name, description, created, modified) VALUES ",
            "(%(id)s, %(name)s, %(description)s, %(created)s, %(modified)s) ",
            "ON CONFLICT (id) DO NOTHING",
        ]
    )
    name: str
    description: str = field(default=None)
    created: datetime.datetime = field(default=None)
    modified: datetime.datetime = field(default=None)
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass
class FilmWork:
    len: ClassVar[int] = 0
    len_query: ClassVar[str] = "SELECT COUNT(*) [int] FROM film_work"
    select_query: ClassVar[str] = "".join(
        [
            "SELECT title [str], description [str], ",
            "creation_date [datetime.date], certificate [str], file_path [str], ",
            "rating [float], type [str], created_at [datetime.datetime], ",
            "updated_at[datetime.datetime], id [uuid.UUID] ",
            "FROM film_work LIMIT ? OFFSET ?",
        ]
    )
    clean_query: ClassVar[str] = "TRUNCATE content.film_work CASCADE"
    insert_query: ClassVar[str] = "".join(
        [
            "INSERT INTO content.film_work ",
            "(title, description, creation_date, ",
            "certificate, file_path, rating, type, ",
            "created, modified, id) ",
            "VALUES (%(title)s, %(description)s, %(creation_date)s, ",
            "%(certificate)s, %(file_path)s, %(rating)s, %(type)s, ",
            "%(created)s, %(modified)s, %(id)s) ",
            "ON CONFLICT (id) DO NOTHING",
        ]
    )
    title: str
    description: str = field(default=None)
    creation_date: datetime.date = field(default=None)
    certificate: str = field(default=None)
    file_path: str = field(default=None)
    rating: float = field(default=0)
    type: str = field(default="movie")
    created: datetime.datetime = field(default=None)
    modified: datetime.datetime = field(default=None)
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass
class Person:
    len: ClassVar[int] = 0
    len_query: ClassVar[str] = "SELECT COUNT(*) [int] FROM person"
    select_query: ClassVar[str] = "".join(
        [
            "SELECT full_name [str], ",
            "birth_date [datetime.date], created_at [datetime.datetime], ",
            "updated_at [datetime.datetime], id [uuid.UUID] ",
            "FROM person LIMIT ? OFFSET ?",
        ]
    )
    clean_query: ClassVar[str] = "TRUNCATE content.person CASCADE"
    insert_query: ClassVar[str] = "".join(
        [
            "INSERT INTO content.person ",
            "(full_name, birth_date, created, modified, id) VALUES ",
            "(%(full_name)s, %(birth_date)s, %(created)s, %(modified)s, %(id)s) ",
            "ON CONFLICT (id) DO NOTHING",
        ]
    )
    full_name: str
    birth_date: datetime.date = field(default=None)
    created: datetime.datetime = field(default=None)
    modified: datetime.datetime = field(default=None)
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass
class GenreFilmWork:
    len: ClassVar[int] = 0
    len_query: ClassVar[str] = "SELECT COUNT(*) [int] FROM genre_film_work"
    select_query: ClassVar[str] = "".join(
        [
            "SELECT film_work_id [str], genre_id [str],",
            " created_at [datetime.datetime], id [uuid.UUID] ",
            "FROM genre_film_work LIMIT ? OFFSET ?",
        ]
    )
    clean_query: ClassVar[str] = "TRUNCATE content.genre_film_work CASCADE"
    insert_query: ClassVar[str] = "".join(
        [
            "INSERT INTO content.genre_film_work ",
            "(film_work_id, genre_id, created, id) ",
            "VALUES (%(film_work_id)s, %(genre_id)s, %(created)s, %(id)s) ",
            "ON CONFLICT (id) DO NOTHING",
        ]
    )
    film_work_id: str
    genre_id: str
    created: datetime.datetime = field(default=None)
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass
class PersonFilmWork:
    len: ClassVar[int] = 0
    len_query: ClassVar[str] = "SELECT COUNT(*) [int] FROM person_film_work"
    select_query: ClassVar[str] = "".join(
        [
            "SELECT film_work_id [str], ",
            "person_id [str], role [str], created_at [datetime.datetime], ",
            "id [uuid.UUID] FROM person_film_work LIMIT ? OFFSET ?",
        ]
    )
    clean_query: ClassVar[str] = "TRUNCATE content.person_film_work CASCADE"
    insert_query: ClassVar[str] = "".join(
        [
            "INSERT INTO content.person_film_work ",
            "(film_work_id, person_id, role, created, id) VALUES ",
            "(%(film_work_id)s, %(person_id)s, %(role)s, %(created)s, %(id)s) ",
            "ON CONFLICT (id) DO NOTHING",
        ]
    )
    film_work_id: str
    person_id: str
    role: str
    created: datetime.datetime = field(default=None)
    id: uuid.UUID = field(default_factory=uuid.uuid4)
