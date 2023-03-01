import uuid
from http import HTTPStatus
from typing import Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from services.film import FilmService, get_film_service

# Объект router, в котором регистрируем обработчики
router = APIRouter()


# FastAPI в качестве моделей использует библиотеку pydantic
# https://pydantic-docs.helpmanual.io
# У неё есть встроенные механизмы валидации, сериализации и десериализации
# Также она основана на дата-классах
class Film(BaseModel):
    # Модель ответа API
    uuid: uuid.UUID
    title: str
    imdb_rating: Optional[float]
    description: Optional[str]
    genre: Optional[List[Dict]]
    actors: Optional[List[Dict]]
    writers: Optional[List[Dict]]
    directors: Optional[List[Dict]]


class FilmList(BaseModel):
    uuid: uuid.UUID
    title: str
    imdb_rating: Optional[float]


# С помощью декоратора регистрируем обработчик film_details
# На обработку запросов по адресу <some_prefix>/some_id
# Позже подключим роутер к корневому роутеру
# И адрес запроса будет выглядеть так — /api/v1/film/some_id
# В сигнатуре функции указываем тип данных,
# получаемый из адреса запроса (film_id: str)
# И указываем тип возвращаемого объекта — Film
# Внедряем FilmService с помощью Depends(get_film_service)
@router.get(
    "/search",
    response_model=List[FilmList],
    summary="Поиск фильмов",
    description="Полнотекстовый поиск по фильмам",
    response_description="Название и рейтинг фильма",
)
async def film_search(
    query: str = "",
    number: int = Query(default=1, alias="page[number]"),
    size: int = Query(default=20, alias="page[size]"),
    film_service: FilmService = Depends(get_film_service),
) -> List[FilmList]:
    films = await film_service.search(query, number, size)
    if not films:
        # Если фильм не найден, отдаём 404 статус
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="film not found")
    return [
        FilmList(
            uuid=uuid.UUID(film.uuid), title=film.title, imdb_rating=film.imdb_rating
        )
        for film in films
    ]


@router.get(
    "/{film_id}",
    response_model=Film,
    summary="Выдача фильма по ID",
    description="Выдача полной информации о фильме по ID",
    response_description="".join(
        ["Название, описание, рейтинг фильма, ", "информация о жанре и персонах"]
    ),
)
async def film_details(
    film_id: str,
    film_service: FilmService = Depends(get_film_service),
) -> Film:
    film = await film_service.get_by_id(film_id)
    if not film:
        # Если фильм не найден, отдаём 404 статус
        # Желательно пользоваться HTTP-статусами, которые содержат enum
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="film not found")

    # Перекладываем данные из models.Film в Film
    return Film(
        uuid=uuid.UUID(film.uuid),
        title=film.title,
        imdb_rating=film.imdb_rating,
        description=film.description,
        genre=film.genre,
        actors=film.actors,
        writers=film.writers,
        directors=film.directors,
    )


@router.get(
    "",
    response_model=List[FilmList],
    summary="Сортировка фильмов",
    description="".join(
        ["Выдача отсортированных по рейтингу фильмов ", "(в общем рейтинге, в жанре)"]
    ),
    response_description="Название и рейтинг фильмов",
)
async def film_sort(
    sort: str = "-imdb_rating",
    number: int = Query(default=1, alias="page[number]"),
    size: int = Query(default=20, alias="page[size]"),
    genre: Optional[str] = None,
    film_service: FilmService = Depends(get_film_service),
) -> List[FilmList]:
    films = await film_service.sort(sort, number, size, genre)
    if not films:
        # Если сортировка не проходит - плохой запрос
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="wrong request")
    return [
        FilmList(
            uuid=uuid.UUID(film.uuid), title=film.title, imdb_rating=film.imdb_rating
        )
        for film in films
    ]
