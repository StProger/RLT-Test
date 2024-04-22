from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    BOT_TOKEN: str

    # Путь к логам
    PATH_LOGS: str = "bot/data/logs.log"

    # Валидные данные
    valid_data: list[dict] = [
        {
            "dt_from": "2022-02-01T00:00:00",
            "dt_upto": "2022-02-02T00:00:00",
            "group_type": "hour"
        },
        {
            "dt_from": "2022-09-01T00:00:00",
            "dt_upto": "2022-12-31T23:59:00",
            "group_type": "month"
        },
        {
            "dt_from": "2022-10-01T00:00:00",
            "dt_upto": "2022-11-30T23:59:00",
            "group_type": "day"
        }
    ]


    class Config:

        env_file = ".env"


settings = Settings()
