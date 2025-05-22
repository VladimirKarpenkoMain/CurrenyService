from typing import Annotated

from fastapi import Depends, Request

from core.currency_service import CurrencyService
from core.store import BalanceStore


def get_store(request: Request) -> BalanceStore:
    store = getattr(request.app.state, "store", None)
    return store


def get_currency_service(
    store: BalanceStore = Depends(get_store),
) -> CurrencyService:
    return CurrencyService(store=store)


CurrencyServiceDep = Annotated[CurrencyService, Depends(get_currency_service)]
