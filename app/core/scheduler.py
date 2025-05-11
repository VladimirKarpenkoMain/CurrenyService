import asyncio
import logging

from app.config import settings
from app.core.fetch_service import FetchService
from app.core.state import CurrencyState, currency_state

logger = logging.getLogger("currency_service")


async def scheduler_fetch(state: CurrencyState, period: int):
    while True:
        try:
            data = await FetchService.fetch_rates()
            state.set_rates(rates=data)
            logger.info("Fetched rates: %s", data)
        except Exception:
            logger.exception("Unknown error fetching rates.")
        await asyncio.sleep(period * 60)


async def scheduler_print():
    while True:
        await asyncio.sleep(
            settings.scheduler_config.print_sleep * 60
        )
        logg_data = currency_state.format_console()
        logger.info(logg_data)
