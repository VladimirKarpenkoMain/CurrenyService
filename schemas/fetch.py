from decimal import Decimal

from pydantic import BaseModel
from typing import Dict


class ValuteResponse(BaseModel):
    Nominal: int
    Name: str
    Value: Decimal


class ExchangeRateResponse(BaseModel):
    Valute: Dict[str, ValuteResponse]
