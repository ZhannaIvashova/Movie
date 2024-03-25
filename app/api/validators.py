from fastapi import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.movie import get_movie_by_id, get_movie_by_name
from app.schemas.movie import MovieCreate, MovieUpdate


async def check_api_response(response):
    """Проверка, что внешний API отдает объект со статус-кодом равным 200"""

    if response.status_code != 200:
        raise HTTPException(
            status_code=response.status_code,
            detail=response.text
        )


async def choice_fields(movie_data: dict) -> dict:
    """Выборка нужных полей из внешнего API-кинопоиска, соответствующих БД"""

    movie_selected = {
            'name': movie_data['nameRu'],
            'country': ', '.join([country['country'] for country in movie_data['countries']]),
            'ratingIMDd': movie_data['ratingImdb'],
            'year': movie_data['year']
        }
    return movie_selected

# эту проверку лучше разделить на две!!!!!!!!!!!!!!!!!!!!!
async def check_name_duplicate(
        movie: str,
        session: AsyncSession,
        source: str,
) -> None:
    """Проверка по имени, что в БД нет одинаковых объектов"""
    movie_obj = await get_movie_by_name(movie, session)

    if movie_obj is not None:
        #если запрос пришел от функции 'create_movie'
        if source == 'create_movie':
            raise HTTPException(
                status_code=422,
                detail=f'Фильм с именем "{movie_obj.name}" уже существует!',
            )
        #если запрос пришел от функции 'get_movie'
        elif source == 'get_movie':
            # Если функция вызвана из get_movie, возвращаю True,
            # что говорит о том что в БД существует такой фильм
            return True


async def check_id_movie(
        movie_id: int,
        session: AsyncSession,
) -> MovieCreate:
    """Проверка по id, что в БД существует данный фильм"""
    movie_obj = await get_movie_by_id(movie_id, session)
    print(movie_obj)

    if movie_obj is None:
        raise HTTPException(
            status_code=404,
            detail='Такой фильм не найден!',
        )
    return movie_obj


async def check_at_least_one_field(
        obj_in: MovieUpdate,
        session: AsyncSession,
) -> MovieUpdate:
    """Проверка, что передано хотя бы одно поле для обновления данных"""
    if not obj_in.model_dump(exclude_none=True):
        raise HTTPException(
            status_code=400,
            detail='Необходимо указать хотя бы одно поле для обновления',
        )
    return obj_in
