from typing import Dict

from pydantic import BaseModel, Field
from typing_extensions import Optional

from app.config import settings


class AmountResponse(BaseModel):
    name: str
    value: float


class AmountUpdateSchema(BaseModel):
    usd: Optional[float] = None
    eur: Optional[float] = None
    rub: Optional[float] = None


for cur in settings.currencies:
    AmountUpdateSchema.__annotations__[cur] = Optional[float]
    setattr(AmountUpdateSchema, cur, None)


class AmountUpdateResponse(BaseModel):
    detail: str


class AmountTotalSchema(BaseModel):
    amounts: Dict[str, float] = Field(
        default_factory=dict,
        examples=[{"USD": 123.45, "EUR": 98.76}],
        description="Количество каждой валюты",
    )
    rates: Dict[str, float] = Field(
        default_factory=dict,
        examples=[{"EUR-USD": 1.3, "USD-EUR": 0.80}],
        description="Курс каждой валюты к базовой",
    )
    total: Dict[str, float] = Field(
        ...,
        examples=[{"USD": 123.45, "EUR": 79.01}],
        description="Итоговая сумма по каждой валюте",
    )
