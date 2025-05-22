from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings


BASE_DIR = Path(__file__).parent.parent


class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000
    count_workers: int = 4


class LoggerConfig(BaseModel):
    logger_name: str = "currency_service"
    log_file: str = BASE_DIR / "app.log"


class FetchConfig(BaseModel):
    fetch_url: str = "https://www.cbr-xml-daily.ru/daily_json.js"
    fetch_timeout: int = 10


class SchedulerConfig(BaseModel):
    print_sleep: int = 1  # Minutes


class Settings(BaseSettings):
    # Run
    run: RunConfig = RunConfig()

    # Init currencies
    currencies: list[str] = [
        "usd",
        "eur",
        "rub",
        "azn",
    ]

    # Logging
    logger: LoggerConfig = LoggerConfig()

    # Fetch
    fetch_config: FetchConfig = FetchConfig()

    # Schedulers
    scheduler_config: SchedulerConfig = SchedulerConfig()


settings = Settings()
