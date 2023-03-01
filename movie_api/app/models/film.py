from typing import Dict, List, Optional

from models.base import BaseModel


class Film(BaseModel):
    uuid: str
    title: str
    imdb_rating: Optional[float]
    description: Optional[str]
    genre: Optional[List[Dict]]
    actors: Optional[List[Dict]]
    writers: Optional[List[Dict]]
    directors: Optional[List[Dict]]
