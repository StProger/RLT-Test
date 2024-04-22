from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    BOT_TOKEN: str

    # Путь к логам
    PATH_LOGS: str = "bot/data/logs.log"

    class Config:

        env_file = ".env"


settings = Settings()
