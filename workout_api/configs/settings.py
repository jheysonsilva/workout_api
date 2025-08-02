from pydantic import Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = Field(
        default='postgresql+asyncpg://workout:workout@localhost/workout',
        env='DATABASE_URL'
    )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
