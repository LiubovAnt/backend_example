import orjson
from pydantic import BaseModel as PudanticBaseModel


def orjson_dumps(v, *, default):
    # orjson.dumps возвращает bytes, а pydantic
    # требует unicode, поэтому декодируем
    return orjson.dumps(v, default=default).decode()


class BaseModel(PudanticBaseModel):
    class Config:
        # Заменяем стандартную работу с json на более быструю
        json_loads = orjson.loads
        json_dumps = orjson_dumps
