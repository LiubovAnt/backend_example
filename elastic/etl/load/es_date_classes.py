from dataclasses import field
from typing import Optional

from pydantic.dataclasses import dataclass


@dataclass
class PersonES:
    uuid: str
    full_name: str
    role: Optional[list] = field(default=None)
    film_ids: Optional[list] = field(default=None)


@dataclass
class GenreES:
    uuid: str
    name: str
    description: str = field(default=None)


@dataclass
class FilmES:
    uuid: str
    title: str
    imdb_rating: float = field(default=None)
    description: str = field(default=None)
    genre: Optional[list] = field(default=None)
    genre_names: Optional[list] = field(default=None)
    actors: Optional[list] = field(default=None)
    actors_names: Optional[list] = field(default=None)
    writers: Optional[list] = field(default=None)
    writers_names: Optional[list] = field(default=None)
    directors: Optional[list] = field(default_factory=[])
    directors_names: Optional[list] = field(default=None)
