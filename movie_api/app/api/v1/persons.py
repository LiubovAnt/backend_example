import uuid
from http import HTTPStatus
from typing import List, Optional

from api.v1.films import FilmList
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from services.film import FilmService, get_film_service
from services.persons import PersonService, get_person_service

# Объект router, в котором регистрируем обработчики
router = APIRouter()


# Модель ответа API
class Person(BaseModel):
    uuid: uuid.UUID
    full_name: str
    role: Optional[List[str]]
    film_ids: Optional[List]


@router.get(
    "/search",
    response_model=List[Person],
    summary="Поиск персон",
    description="Полнотекстовый поиск по персонам",
    response_description="Полное имя, роль и id фильмов",
)
async def person_search(
    query: str = "",
    number: int = Query(default=1, alias="page[number]"),
    size: int = Query(default=20, alias="page[size]"),
    person_service: PersonService = Depends(get_person_service),
) -> List[Person]:
    persons = await person_service.search(query, number, size)

    if not persons:
        # Если фильм не найден, отдаём 404 статус
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="person not found")

    return [
        Person(
            uuid=uuid.UUID(person.uuid),
            full_name=person.full_name,
            role=person.role,
            film_ids=person.film_ids,
        )
        for person in persons
    ]


@router.get(
    "/{person_id}/film",
    response_model=List[FilmList],
    summary="Выдача фильмов персоны по ID",
    description="Выдача фильмов персоны по ID",
    response_description="Название и рейтинг фильмов",
)
async def person_films(
    person_id: str,
    person_service: PersonService = Depends(get_person_service),
    film_service: FilmService = Depends(get_film_service),
) -> List[FilmList]:
    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="person not found")
    films = await film_service.get_by_ids(person.film_ids)
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="films not found")
    return [
        FilmList(
            uuid=uuid.UUID(film.uuid),
            title=film.title,
            imdb_rating=film.imdb_rating,
        )
        for film in films
    ]


@router.get(
    "/{person_id}",
    response_model=Person,
    summary="Выдача персоны по ID",
    description="Выдача персоны по ID",
    response_description="Полное имя, роль и ID фильмов",
)
async def person_details(
    person_id: str,
    person_service: PersonService = Depends(get_person_service),
) -> Person:
    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="person not found")
    return Person(
        uuid=uuid.UUID(person.uuid),
        full_name=person.full_name,
        role=person.role,
        film_ids=person.film_ids,
    )
