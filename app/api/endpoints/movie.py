from fastapi import APIRouter, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_name_duplicate, check_id_movie, check_at_least_one_field
)
from app.core.db import get_async_session
from app.crud.movie import create, delete_movie, update_movie
from app.schemas.movie import MovieCreate, MovieDB, MovieUpdate

router = APIRouter()


@router.post('/', response_model=MovieCreate)
async def create_movie(
    new_movie: MovieCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """Создание фильма"""

    await check_name_duplicate(new_movie.name, session, source='create_movie')
    new_movie = await create(new_movie, session)
    return new_movie


@router.patch('/{movie_id}', response_model=MovieDB)
async def partial_movie_update(
    movie_id: int,
    # JSON-данные, отправленные пользователем
    obj_in: MovieUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    """Обновление данных фильма"""
    await check_at_least_one_field(obj_in, session)
    movie_obj = await check_id_movie(movie_id, session)
    movie = await update_movie(movie_obj, obj_in, session)
    return movie



@router.delete('/{movie_id}', response_model=MovieCreate)
async def remove_movie(
    movie_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    """Удаление фильма"""
    movie = await delete_movie(movie_id, session)
    return movie
