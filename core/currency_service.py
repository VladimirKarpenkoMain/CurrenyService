from decimal import Decimal
from typing import Dict

from fastapi import HTTPException, status

from core.store import BalanceStore
from utils.abstracts import AbstractCurrencyService
from schemas.currency import AmountResponse, AmountUpdateSchema


class CurrencyService(AbstractCurrencyService):
    """
    Сервис для работы с валютами, предоставляющий методы для получения, установки и изменения количества валют,
    а также для получения сводной информации.
    """

    def __init__(self, store: BalanceStore) -> None:
        """
        Инициализирует экземпляр класса CurrencyService.

        :param store: Экземпляр класса BalanceStore для хранения и управления данными о валютах.
        """
        self._store = store

    def get_by_code(self, currency_code: str) -> AmountResponse:
        """
        Получает информацию о валюте по её коду.

        :param currency_code: Код валюты (например, "USD").
        :return: Объект AmountResponse с названием валюты и её текущим количеством.
        :raises HTTPException: Если валюта не поддерживается (код 404).
        """
        currency_code = currency_code.upper()
        if currency_code not in self._store.amounts:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Currency not supported",
            )

        currency_amount = self._store.get_amount(currency_code=currency_code)
        return AmountResponse(name=currency_code, value=currency_amount)

    def set_amount(self, set_amount: AmountUpdateSchema) -> None:
        """
        Устанавливает новое количество для указанных валют.

        :param set_amount: Схема AmountUpdateSchema с информацией о валютах и их новых количествах.
        """
        set_amount_dict = set_amount.model_dump()
        self._store.set_amount(new_amounts=set_amount_dict)

    def modify_amount(self, modify_amount: AmountUpdateSchema) -> None:
        """
        Изменяет количество указанных валют на заданную величину.

        :param modify_amount: Схема AmountUpdateSchema с информацией о валютах и величинах изменения их количества.
        """
        try:
            modify_amount_dict = modify_amount.model_dump()
            self._store.modify_amount(modify_amounts=modify_amount_dict)
        except ValueError as e:
            code = e.args[1]
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"The amount of currency cannot be less than zero: {code}",
            )

    def get_total_info(self) -> Dict[str, Dict[str, Decimal]]:
        """
        Получает сводную информацию о всех валютах, включая их количества, курсы обмена и общие суммы в базовых валютах.

        :return: Словарь с ключами "amounts", "rates" и "total", содержащий соответствующие данные.
        """
        return self._store.summary()
