from sqlalchemy import Column, Float, Integer, String

# базовый класс для моделей
from app.core.db import Base


class Movie(Base):
    name = Column(String(100), unique=True, nullable=False)
    country = Column(String)
    ratingIMDd = Column(Float)
    year = Column(Integer)