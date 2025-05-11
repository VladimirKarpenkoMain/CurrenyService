from pydantic import BaseModel
from typing import Dict


class ValuteResponse(BaseModel):
    Nominal: int
    Name: str
    Value: float


class ExchangeRateResponse(BaseModel):
    Valute: Dict[str, ValuteResponse]
