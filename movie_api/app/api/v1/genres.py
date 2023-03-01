import uuid
from http import HTTPStatus
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from services.genres import GenreService, get_genre_service

# Объект router, в котором регистрируем обработчики
router = APIRouter()


# Модель ответа API
class Genre(BaseModel):
    uuid: uuid.UUID
    name: str
    description: Optional[str]


@router.get(
    "/{genre_id}",
    response_model=Genre,
    summary="Выдача жанра по ID",
    description="Выдача названия и описания жанра по ID",
    response_description="Название и описание жанра",
)
async def genre_details(
    genre_id: str,
    genre_service: GenreService = Depends(get_genre_service),
) -> Genre:
    genre = await genre_service.get_by_id(genre_id)
    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="genre not found")
    print(genre)
    return Genre(
        uuid=uuid.UUID(genre.uuid), name=genre.name, description=genre.description
    )


@router.get(
    "",
    response_model=List[Genre],
    summary="Выдача полного списка жанров",
    description="".join(["Выдача полного списка жанров ", "с названиями и описанием"]),
    response_description="".join(["Полный список жанров ", "с названиями и описанием"]),
)
async def genre_list(
    genre_service: GenreService = Depends(get_genre_service),
) -> List[Genre]:
    genres = await genre_service.get_list()
    if not genres:
        # Если фильм не найден, отдаём 404 статус
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="genre not found")

    return [
        Genre(
            uuid=uuid.UUID(genre.uuid), name=genre.name, description=genre.description
        )
        for genre in genres
    ]
