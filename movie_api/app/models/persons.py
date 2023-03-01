from typing import List, Optional

from models.base import BaseModel


class Person(BaseModel):
    uuid: str
    full_name: str
    role: Optional[List[str]]
    film_ids: Optional[List]
