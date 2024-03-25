from fastapi.encoders import jsonable_encoder

from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

#from app.api.validators import check_name_duplicate
#from app.core.db import AsyncSessionLocal, get_async_session
from app.models.movie import Movie
from app.schemas.movie import MovieCreate, MovieUpdate

'''
#эту функцию можно полностью игнорировать и использовать для сохранение объектов от стороннего api функцию create, но нужно учесть, что при попытки двух объектов в бз, нужно сделать валидацию на проверку их в бз, и игнорировать, а в ф-ции create есть такая проверка, но с выводом сообщения
async def create_movie_from_api(
    new_movie: dict,
    session: AsyncSession,
) -> MovieCreate:
    """Cоздание фильмов в БД (от стороннего API)"""

    # Конвертируем объект MovieCreate в словарь.
    new_movie_data = new_movie.dict()

    # СДЕЛАТЬ ПРОВЕРКУ НА ПОВТОР ФИЛЬМА В БД!!!!!!!!!!!!!!!!!!!!!!
    #check_name_duplicate(new_movie_data.name)

    # Создаём объект модели Movie.
    # В параметры передаём пары "ключ=значение", для этого распаковываем словарь.
    db_movie = Movie(**new_movie_data)
    #async with AsyncSessionLocal() as session:
        #session.add(db_movie)
        #await session.commit()
        #await session.refresh(db_movie)
    print(db_movie)
    session.add(db_movie)
    await session.commit()
    await session.refresh(db_movie)
    # Возвращаем только что созданный объект класса Movie.
    #return db_movie
    return MovieCreate.model_validate(db_movie) #from_orm устарел!!!
'''


async def create(
    new_movie: dict,
    session: AsyncSession,
) -> MovieCreate:
    """Cоздание фильмов в БД (напрямую от пользователя)"""

    new_movie_data = new_movie.dict() 
    db_movie = Movie(**new_movie_data)
    session.add(db_movie)
    await session.commit()
    await session.refresh(db_movie)
    #return db_movie
    return MovieCreate.model_validate(db_movie)


async def get_movie_by_name(
    movie: str,
    session: AsyncSession,
) -> Optional[Movie]:
    """Поиск объекта в БД по имени"""

    db_movie = await session.execute(select(Movie).where(Movie.name == movie))
    db_movie_obj = db_movie.scalars().first()
    return db_movie_obj


async def get_movie_by_id(
    movie_id: int,
    session: AsyncSession,
) -> Optional[Movie]:
    """Поиск объекта в БД по id"""

    db_movie = await session.execute(select(Movie).where(Movie.id == movie_id))
    db_movie_obj = db_movie.scalars().first()
    return db_movie_obj


async def update_movie(
    db_movie: Movie,
    obj_in: MovieUpdate,
    session: AsyncSession,
) -> MovieCreate:
    """Обновление фильмов в БД"""
    # Конвертирую объект из БД в словарь Python
    db_movie_data = jsonable_encoder(db_movie)
    updata_movie_data = obj_in.dict(exclude_unset=True)

    for field in db_movie_data:
        if field in updata_movie_data:
            setattr(db_movie, field, updata_movie_data[field])
    session.add(db_movie)
    await session.commit()
    await session.refresh(db_movie)

    return db_movie


async def delete_movie(
    movie_id: int,
    session: AsyncSession,
):
    """Удаление объекта из БД по id"""

    db_movie = await session.execute(select(Movie).where(Movie.id == movie_id))
    movie = db_movie.scalars().first()
    print(movie)
    await session.delete(movie)
    await session.commit()
    return movie
