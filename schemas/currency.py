from decimal import Decimal
from typing import Dict

from pydantic import BaseModel, Field, create_model
from typing_extensions import Optional

from core.config import settings


class AmountResponse(BaseModel):
    name: str
    value: Decimal


amount_set_fields = {
    cur: (Optional[Decimal], Field(None, ge=0)) for cur in settings.currencies
}
AmountSetSchema = create_model("AmountSetSchema", **amount_set_fields)

amount_update_fields = {cur: (Optional[Decimal], None) for cur in settings.currencies}
AmountUpdateSchema = create_model("AmountUpdateSchema", **amount_update_fields)


class AmountUpdateResponse(BaseModel):
    detail: str


class AmountTotalSchema(BaseModel):
    amounts: Dict[str, Decimal] = Field(
        default_factory=dict,
        examples=[{"USD": 123.45, "EUR": 98.76}],
        description="Количество каждой валюты",
    )
    rates: Dict[str, Decimal] = Field(
        default_factory=dict,
        examples=[{"EUR-USD": 1.3, "USD-EUR": 0.80}],
        description="Курс каждой валюты к базовой",
    )
    total: Dict[str, Decimal] = Field(
        ...,
        examples=[{"USD": 123.45, "EUR": 79.01}],
        description="Итоговая сумма по каждой валюте",
    )
