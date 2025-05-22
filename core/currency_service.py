from typing import Dict

from fastapi import HTTPException

from app.utils.abstracts import AbstractCurrencyService
from app.core.state import currency_state, CurrencyState
from app.schemas.currency import AmountResponse, AmountUpdateSchema


class CurrencyService(AbstractCurrencyService):
    state: CurrencyState = currency_state

    @classmethod
    def get_by_code(cls, currency_code: str) -> AmountResponse:
        currency_code = currency_code.upper()
        if currency_code not in cls.state.amounts:
            raise HTTPException(
                status_code=404,
                detail="Currency not supported",
            )

        currency_amount = cls.state.get_amount(currency_code=currency_code)
        return AmountResponse(name=currency_code, value=currency_amount)

    @classmethod
    def set_amount(cls, set_amount: AmountUpdateSchema) -> None:
        set_amount_dict = set_amount.model_dump()
        cls.state.set_amount(new_amounts=set_amount_dict)

    @classmethod
    def modify_amount(cls, modify_amount: AmountUpdateSchema) -> None:
        modify_amount_dict = modify_amount.model_dump()
        cls.state.modify_amount(modify_amounts=modify_amount_dict)

    @classmethod
    def get_total_info(cls) -> Dict[str, Dict[str, float]]:
        return cls.state.summary()
