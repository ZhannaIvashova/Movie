from fastapi import APIRouter

from app.api.endpoints import outside_api_router, movie_router

main_router = APIRouter()
main_router.include_router(
    outside_api_router,
    prefix='/api/v2.2/films/collections',
    tags=['Movies from outside api']
)
main_router.include_router(
    movie_router,
    prefix='/movie',
    tags=['Movies']
)
