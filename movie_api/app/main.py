import logging

import aioredis
import uvicorn
from api.v1 import films, genres, persons
from core import config
from core.logger import LOGGING
from db import elastic, redis
from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

app = FastAPI(
    title="Read-only API для онлайн-кинотеатра",
    description="".join(
        [
            "Информация о фильмах, жанрах и людях, участвовавших ",
            "в создании произведения",
        ]
    ),
    version="1.0.0",
    docs_url="/movie/api/v1/docs",
    openapi_url="/movie/api/openapi.json",
    default_response_class=ORJSONResponse,
)


@app.on_event("startup")
async def startup():
    redis.redis = await aioredis.create_redis_pool(
        (config.REDIS_HOST, config.REDIS_PORT), minsize=10, maxsize=20
    )
    elastic.es = AsyncElasticsearch(
        hosts=[
            "{host}:{port}".format(host=config.ELASTIC_HOST, port=config.ELASTIC_PORT)
        ]
    )


@app.on_event("shutdown")
async def shutdown():
    await redis.redis.close()
    await elastic.es.close()


# Подключаем роутер к серверу, указав префикс /v1/films
# Теги указываем для удобства навигации по документации
app.include_router(films.router, prefix="/movie/api/v1/films", tags=["film"])
app.include_router(genres.router, prefix="/movie/api/v1/genres", tags=["genres"])
app.include_router(persons.router, prefix="/movie/api/v1/persons", tags=["persons"])

if __name__ == "__main__":
    logging.config.dictConfig(LOGGING)
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
    )
