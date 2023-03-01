import datetime
import uuid
from dataclasses import field
from typing import ClassVar

from extract import sql_query
from pydantic.dataclasses import dataclass


@dataclass
class ProducterData:
    query: ClassVar[str] = sql_query.producter
    query_modified: ClassVar[str] = sql_query.modified
    query_count: ClassVar[str] = sql_query.producer_count
    id: uuid.UUID
    modified: datetime.datetime = field(default=None)


@dataclass
class EnricherData:
    query: ClassVar[str] = sql_query.enricher
    query_fw: ClassVar[str] = sql_query.enricher_fw
    query_count: ClassVar[str] = sql_query.enricher_count
    query_count_fw: ClassVar[str] = sql_query.enricher_count_fw
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    modified: datetime.datetime = field(default=None)


@dataclass
class PersonSQL:
    query: ClassVar[str] = sql_query.person
    id: uuid.UUID
    full_name: str
    modified: datetime.datetime = field(default=None)
    role: str = field(default=None)
    film_ids: uuid.UUID = field(default=None)


@dataclass
class GenreSQL:
    query: ClassVar[str] = sql_query.genre
    id: uuid.UUID
    name: str
    description: str = field(default=None)
    modified: datetime.datetime = field(default=None)


@dataclass
class FilmSQL:
    query: ClassVar[str] = sql_query.film
    title: str
    id: uuid.UUID
    imdb_rating: float = field(default=None)
    genre: str = field(default=None)
    genre_id: uuid.UUID = field(default=None)
    description: str = field(default=None)
    type: str = field(default=None)
    created: datetime.datetime = field(default=None)
    modified: datetime.datetime = field(default=None)
    role: str = field(default=None)
    person_id: uuid.UUID = field(default=None)
    full_name: str = field(default=None)
