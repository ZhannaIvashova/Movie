from fastapi import FastAPI

from app.api.routers import main_router


app = FastAPI(title='Проект о кино', description='Новое приложение')

app.include_router(main_router)

#uvicorn app.main:app --reload
#http://127.0.0.1:8000/docs