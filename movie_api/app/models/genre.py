from typing import Optional

from models.base import BaseModel


class Genre(BaseModel):
    uuid: str
    name: str
    description: Optional[str]
