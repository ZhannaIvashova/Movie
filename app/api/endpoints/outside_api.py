import httpx
import random

from fastapi import APIRouter, Depends
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.db import get_async_session
from app.crud.movie import create
from app.api.validators import check_api_response, choice_fields, check_name_duplicate
from app.schemas.movie import MovieCreate

router = APIRouter()

@router.get('/', response_model=List[MovieCreate])
async def get_movie(
    session: AsyncSession = Depends(get_async_session)
):
    random_page = random.randint(1, 35)

    headers = {
        "x-api-key": settings.api_key,
        "accept": "application/json"
    }
    params = {
        "type": 'TOP_POPULAR_MOVIES',
        "page": random_page
    }
    # асинхронный GET запрос к URL внешнего API, с передачей данных
    async with httpx.AsyncClient() as client:
        response = await client.get(
            settings.api_url,
            headers=headers,
            params=params,
            #follow_redirects=False
        )
        await check_api_response(response)
        # дессериализация из json в python словарь
        movie_data = response.json()

        # эти две строчки потом удалить, тк проверяю что рандомно выбранные фильмы есть в списке
        #list_movies = [movie['nameRu'] for movie in movie_data['items']]
        #print(list_movies)

        movie_first = random.choice(movie_data['items'])
        movie_second = random.choice(movie_data['items'])
        while movie_second['nameRu'] == movie_first['nameRu']:
            movie_second = random.choice(movie_data['items'])

        #Передаю данные в функцию выбирающую нужные поля
        movie_first_selected = await choice_fields(movie_first)
        movie_second_selected = await choice_fields(movie_second)

        #Преобразую полученный словарь в Pydantic-модель
        movie_one_data = MovieCreate(**movie_first_selected)
        movie_two_data = MovieCreate(**movie_second_selected)

        movie_one = await check_name_duplicate(movie_one_data.name, session, source='get_movie')
        movie_two = await check_name_duplicate(movie_two_data.name, session, source='get_movie')

        if movie_one is not True:
        # Передаю данные в корутину создания объекта фильма
            await create(movie_one_data, session)
        if movie_two is not True:
            await create(movie_two_data, session)

        return [movie_one_data, movie_two_data]
