from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    api_key: str
    api_url: str
    database_url: str
    #secret_key: str = 'SECRET_KEY'

    class Config:
        env_file = '.env'


settings = Settings()
