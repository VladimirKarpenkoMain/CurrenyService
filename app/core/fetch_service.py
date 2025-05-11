import logging

import httpx

from app.config import settings
from app.schemas.fetch import ExchangeRateResponse
from app.utils.abstracts import AbstractFetchService

logger = logging.getLogger(settings.logger.logger_name)


class FetchService(AbstractFetchService):
    @classmethod
    async def fetch_rates(cls):
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    settings.fetch_config.fetch_url,
                    timeout=settings.fetch_config.fetch_timeout,
                )
                response.raise_for_status()
                data = response.json()
            except Exception as e:
                logger.exception(
                    "Unknown error when trying to make a httpx request: %s", e
                )

        parsed = ExchangeRateResponse(**data)
        rates = dict()
        for currency in settings.currencies:
            try:
                if currency != "rub":
                    currency = currency.upper()
                    rates[currency] = parsed.Valute[currency].Value
            except KeyError:
                logger.exception(
                    "There is no such currency code in the parsed data."
                )
        rates["RUB"] = 1.0
        return rates
