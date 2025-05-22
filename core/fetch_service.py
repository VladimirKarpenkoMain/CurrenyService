import logging
from decimal import Decimal

import httpx

from core.config import settings
from schemas.fetch import ExchangeRateResponse
from utils.abstracts import AbstractFetchService

logger = logging.getLogger(settings.logger.logger_name)


class FetchService(AbstractFetchService):
    """
    Сервис для получения курсов валют с внешнего API.
    """

    def __init__(self):
        """
        Инициализирует экземпляр класса FetchService.
        """
        self.client = httpx.AsyncClient()

    async def fetch_rates(self):
        """
        Получает курсы валют с внешнего API.

        :return: Словарь с кодами валют и их курсами.
        :raises Exception: Если произошла ошибка при выполнении запроса или парсинге данных.
        """
        try:
            response = await self.client.get(
                settings.fetch_config.fetch_url,
                timeout=settings.fetch_config.fetch_timeout,
            )
            response.raise_for_status()
            data = response.json()
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
            rates["RUB"] = Decimal(1.0)
            return rates
        except Exception as e:
            logger.exception("Unknown error when trying to make a httpx request: %s", e)
            raise

    async def aclose(self):
        """
        Закрывает HTTP-клиент.
        """
        await self.client.aclose()
