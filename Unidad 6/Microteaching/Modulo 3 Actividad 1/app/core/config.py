from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    DATABASE_URL: str

    class Config:
        env_file = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            ".env"
        )
        env_file_encoding = "utf-8"


settings = Settings()