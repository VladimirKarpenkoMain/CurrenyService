import asyncio
import logging
from decimal import Decimal
from typing import Dict

import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI

from api import api_router
from core import FetchService
from core.config import settings
from core.store import BalanceStore
from utils.logger import setup_logging
from utils.cli import parse_args
from utils.abstracts import AbstractFetchService
from core.scheduler import scheduler_fetch, scheduler_print
from core.middleware import register_middleware

logger = logging.getLogger(settings.logger.logger_name)


def create_app(period: int, init_amount: Dict[str, Decimal]) -> FastAPI:
    """ Функция для создания и конфигурирования FastAPI приложения.

    Инициализирует основные компоненты системы:
    - Хранилище балансов (BalanceStore)
    - Сервис получения данных (FetchService)
    - Фоновые задачи обновления и отображения данных
    - API роутеры

    Args:
        period: Интервал обновления данных в секундах
        init_amount: Начальные балансы валют в формате {ВАЛЮТА: сумма}

    Returns:
        Сконфигурированный экземпляр FastAPI приложения
    """

    store: BalanceStore = BalanceStore()
    store.init_amount(amounts=init_amount)
    fetch: AbstractFetchService = FetchService()

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        # Запуск приложения
        logger.info("App started")
        app.state.store = store
        app.state.fetch = fetch
        app.state._fetch_task = asyncio.create_task(
            scheduler_fetch(store=store, fetch_service=fetch, period=period)
        )
        app.state._print_task = asyncio.create_task(scheduler_print(store=store))

        yield
        # Завершение приложения
        app.state._fetch_task.cancel()
        app.state._print_task.cancel()
        await app.state._fetch_task
        await app.state._print_task
        await app.state.fetch.aclose()
        logger.info("App finished")

    app = FastAPI(lifespan=lifespan)
    app.include_router(api_router)
    return app


def main():
    args = parse_args()

    setup_logging(args.debug)

    init_state = {}
    for currency in settings.currencies:
        attr = getattr(args, currency)
        init_state[currency.upper()] = Decimal(attr)

    app = create_app(period=args.period, init_amount=init_state)
    if args.debug:
        register_middleware(app)

    uvicorn.run(
        app=app,
        host=settings.run.host,
        port=settings.run.port,
        # workers=settings.run.count_workers,
        # reload=True if args.debug else False,
    )


if __name__ == "__main__":
    main()
