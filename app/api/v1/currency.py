from fastapi import APIRouter

from app.core.currency_service import CurrencyService
from app.schemas.currency import (
    AmountResponse,
    AmountUpdateSchema,
    AmountUpdateResponse,
    AmountTotalSchema,
)

router = APIRouter()


@router.get(
    path="/{currency}/get/",
    response_model=AmountResponse,
)
async def get_currency(currency: str):
    return CurrencyService.get_by_code(currency_code=currency)


@router.get(
    path="/amount/get/",
    response_model=AmountTotalSchema,
)
async def get_amount():
    return CurrencyService.get_total_info()


@router.post(
    path="/amount/set/",
    response_model=AmountUpdateResponse,
)
async def set_amount(update_amount: AmountUpdateSchema):
    CurrencyService.set_amount(set_amount=update_amount)
    return AmountUpdateResponse(
        detail="The number of currencies has been successfully updated."
    )


@router.post(
    path="/modify/",
    response_model=AmountUpdateResponse,
)
async def modify_amount(update_amount: AmountUpdateSchema):
    CurrencyService.modify_amount(modify_amount=update_amount)
    return AmountUpdateResponse(
        detail="The number of currencies has been successfully updated."
    )
