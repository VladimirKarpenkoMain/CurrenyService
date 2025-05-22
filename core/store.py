from decimal import Decimal
from typing import Dict
import logging

from core.config import settings

logger = logging.getLogger(settings.logger.logger_name)

# TODO: можно добавить кеширование


class BalanceStore:
    """
    Класс для хранения и управления данными о валютах, включая их количества и курсы обмена.
    """

    def __init__(self):
        """
        Инициализирует экземпляр класса BalanceStore.
        """
        self.amounts: Dict[str, Decimal] = {}
        self.rates: Dict[str, Decimal] = {}
        self._changed = False

    def _check_amount(self, code, new_amount):
        """
        Проверяет, не станет ли количество валюты отрицательным после изменения.

        :param code: Код валюты.
        :param new_amount: Величина изменения количества.
        :raises ValueError: Если количество станет отрицательным.
        """
        if self.amounts[code] + new_amount < 0:
            raise ValueError("The amount of currency cannot be less than zero", code)

    def set_changed(self) -> None:
        """
        Устанавливает флаг изменения данных.
        """
        self._changed = True

    def log_changed(self) -> None:
        """
        Логирует изменения данных, если они произошли.
        """
        if self._changed:
            console = self.format_console()
            logger.info("Currency changed: %s", console)
            self._changed = False

    def data_change(self) -> None:
        """
        Отмечает, что данные были изменены, и логирует это.
        """
        self.set_changed()
        self.log_changed()

    def set_rates(self, rates: Dict[str, Decimal]) -> None:
        """
        Устанавливает курсы обмена для валют.

        :param rates: Словарь с кодами валют и их курсами.
        """
        self.rates = rates
        self.data_change()

    def init_amount(self, amounts: Dict[str, Decimal]) -> None:
        """
        Инициализирует количества валют.

        :param amounts: Словарь с кодами валют и их начальными количествами.
        """
        self.amounts = {cur.upper(): amount for cur, amount in amounts.items()}

    def get_amount(self, currency_code: str) -> Decimal:
        """
        Получает текущее количество указанной валюты.

        :param currency_code: Код валюты.
        :return: Количество валюты в виде Decimal.
        """
        return self.amounts.get(currency_code)

    def set_amount(self, new_amounts: Dict[str, Decimal]) -> None:
        """
        Устанавливает новые количества для указанных валют.

        :param new_amounts: Словарь с кодами валют и их новыми количествами.
        """
        for code, amount in new_amounts.items():
            self.amounts[code.upper()] = amount
        self.data_change()

    def modify_amount(self, modify_amounts: Dict[str, Decimal]) -> None:
        """
        Изменяет количества указанных валют на заданные величины.

        :param modify_amounts: Словарь с кодами валют и величинами изменения их количества.
        """
        for code, amount in modify_amounts.items():
            code = code.upper()
            self._check_amount(code, amount)
            self.amounts[code] = self.amounts.get(code, 0) + amount
        self.data_change()

    def summary(self) -> Dict[str, Dict[str, Decimal]]:
        """
        Возвращает сводную информацию о валютах, включая их количества, курсы обмена и общие суммы в базовых валютах.

        :return: Словарь с ключами "amounts", "rates" и "total".
        """
        summary = {"amounts": dict(self.amounts)}
        pair_rates = {
            f"{c2}-{c1}": round(self.rates[c2] / self.rates[c1], 4)
            for c1 in self.amounts
            for c2 in self.amounts
            if c1 != c2
        }
        result_rates = {pair: pair_rates[pair] for pair in sorted(pair_rates)}

        totals: Dict[str, float] = {}
        for base in self.rates:
            total = sum(
                self.amounts[c] * self.rates[c] / self.rates[base] for c in self.amounts
            )
            totals[base] = round(total, 4)

        summary["rates"] = result_rates
        summary["total"] = totals
        return summary

    def format_console(self) -> str:
        """
        Форматирует сводную информацию для вывода в консоль.

        :return: Строковое представление сводной информации.
        """
        summary_data = self.summary()

        lines: list[str] = []
        for cur, amount in summary_data["amounts"].items():
            lines.append(f"{cur.lower()}: {amount}")
        lines.append("")

        for pair, val in summary_data["rates"].items():
            lines.append(f"{pair.lower()}: {val}")
        lines.append("")

        total = summary_data["total"]
        parts = [f"{total[cur]:.4f} {cur.lower()}" for cur in summary_data["amounts"]]
        lines.append("sum: " + " / ".join(parts))

        return "\n".join(lines)
