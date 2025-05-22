import asyncio
import logging

from core.config import settings
from core.store import BalanceStore
from utils.abstracts import AbstractFetchService

logger = logging.getLogger("currency_service")


async def scheduler_fetch(
    store: BalanceStore,
    fetch_service: AbstractFetchService,
    period: int,
):
    """
    Периодически получает курсы валют и обновляет их в хранилище.

    :param store: Экземпляр BalanceStore для хранения данных о валютах.
    :param fetch_service: Сервис для получения курсов валют.
    :param period: Период обновления в минутах.
    """
    try:
        while True:
            data = await fetch_service.fetch_rates()
            store.set_rates(rates=data)
            logger.info("Fetched rates: %s", data)
            await asyncio.sleep(period * 60)
    except asyncio.CancelledError:
        return


async def scheduler_print(store: BalanceStore):
    """
    Периодически выводит в лог сводную информацию о валютах.

    :param store: Экземпляр BalanceStore для хранения данных о валютах.
    """
    try:
        while True:
            await asyncio.sleep(settings.scheduler_config.print_sleep * 60)
            logg_data = store.format_console()
            logger.info(logg_data)
    except asyncio.CancelledError:
        return
