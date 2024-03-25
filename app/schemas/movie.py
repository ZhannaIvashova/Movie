from typing import Optional

from pydantic import BaseModel, Field, validator


class MovieCreate(BaseModel):
    name: str
    country: Optional[str]
    ratingIMDd: Optional[float]
    year: Optional[int]

    class Config:
        from_attributes = True


class MovieUpdate(BaseModel):
    # Указываю, что поля может не быть
    name: Optional[str] = Field(None)
    country: Optional[str] = Field(None)
    ratingIMDd: Optional[float] = Field(None)
    year: Optional[int] = Field(None)

    @validator('name')
    def name_cannot_be_null(cls, value):
        if value is None:
            raise ValueError('Название фильма не может быть пустым (равным null)!')
        return value


class MovieDB(MovieCreate):
    id: int
