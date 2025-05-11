from typing import Dict
import logging

from app.config import settings

logger = logging.getLogger(settings.logger.logger_name)

# TODO: можно добавить кеширование

class CurrencyState:
    def __init__(self):
        self.amounts: Dict[str, float] = {}
        self.rates: Dict[str, float] = {}
        self._changed = False

    def set_changed(self) -> None:
        self._changed = True

    def log_changed(self) -> None:
        if self._changed:
            console = self.format_console()
            logger.info("Currency changed: %s", console)
            self._changed = False

    def data_change(self) -> None:
        self.set_changed()
        self.log_changed()

    def set_rates(self, rates: Dict[str, float]) -> None:
        self.rates = rates
        self.data_change()

    def init_amount(self, amounts: Dict[str, float]) -> None:
        self.amounts = {
            cur.upper(): amount for cur, amount in amounts.items()
        }

    def get_amount(self, currency_code: str) -> float:
        return self.amounts.get(currency_code)

    def set_amount(self, new_amounts: Dict[str, float]) -> None:
        for code, amount in new_amounts.items():
            self.amounts[code.upper()] = amount
        self.data_change()

    def modify_amount(self, modify_amounts: Dict[str, float]) -> None:
        for code, amount in modify_amounts.items():
            code = code.upper()
            self.amounts[code] = self.amounts.get(code, 0) + amount
        self.data_change()

    def summary(self) -> Dict[str, Dict[str, float]]:
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
                self.amounts[c] * self.rates[c] / self.rates[base]
                for c in self.amounts
            )
            totals[base] = round(total, 4)

        summary["rates"] = result_rates
        summary["total"] = totals
        return summary

    def format_console(self) -> str:
        summary_data = self.summary()

        lines: list[str] = []
        for cur, amount in summary_data["amounts"].items():
            lines.append(f"{cur.lower()}: {amount}")
        lines.append("")

        for pair, val in summary_data["rates"].items():
            lines.append(f"{pair.lower()}: {val}")
        lines.append("")

        total = summary_data["total"]
        parts = [
            f"{total[cur]:.4f} {cur.lower()}"
            for cur in summary_data["amounts"]
        ]
        lines.append("sum: " + " / ".join(parts))

        return "\n".join(lines)


currency_state = CurrencyState()
