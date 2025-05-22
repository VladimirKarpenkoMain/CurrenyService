from fastapi import APIRouter

from core.dependencies import CurrencyServiceDep
from schemas.currency import (
    AmountResponse,
    AmountSetSchema,
    AmountUpdateSchema,
    AmountUpdateResponse,
    AmountTotalSchema,
)

router = APIRouter()


@router.get(
    path="/amount/get/",
    response_model=AmountTotalSchema,
    summary="Получение общей информации о валютах",
    description="Возвращает текущие суммы валют, их курсы и итоговые значения в базовой валюте.",
    responses={500: {"description": "Internal Server Error"}},
)
async def get_amount(
    currency_service: CurrencyServiceDep,
):
    """
    Получает общую информацию о валютах и их курсах.

    Возвращает данные о текущих суммах валют, их курсах относительно базовой валюты
    и итоговую сумму для каждой валюты в формате, соответствующем OpenAPI.

    Args:
        currency_service (CurrencyServiceDep): Зависимость сервиса валют для обработки запроса.

    Returns:
        AmountTotalSchema: Объект, содержащий суммы валют, курсы и итоговые значения.

    Raises:
        HTTPException: В случае внутренней ошибки сервера (status_code=500).
    """
    return currency_service.get_total_info()


@router.get(
    path="/{currency}/get/",
    response_model=AmountResponse,
    summary="Получение информации о конкретной валюте",
    description="Возвращает название и текущую сумму указанной валюты по её коду.",
    responses={
        404: {"description": "Currency not supported"},
        500: {"description": "Internal Server Error"},
    },
)
async def get_currency(
    currency: str,
    currency_service: CurrencyServiceDep,
):
    """
    Получает информацию о конкретной валюте по её коду.

    Возвращает данные о валюте, включая её название и текущую сумму, в формате, соответствующем OpenAPI.

    Args:
        currency (str): Код валюты (например, USD, EUR, RUB).
        currency_service (CurrencyServiceDep): Зависимость сервиса валют для обработки запроса.

    Returns:
        AmountResponse: Объект, содержащий название и сумму указанной валюты.

    Raises:
        HTTPException: Если валюта не найдена (status_code=404) или произошла внутренняя ошибка сервера (status_code=500).
    """
    return currency_service.get_by_code(currency_code=currency)


@router.post(
    path="/amount/set/",
    response_model=AmountUpdateResponse,
    summary="Установка новых сумм валют",
    description="Устанавливает новые значения сумм для указанных валют.",
    responses={
        200: {"description": "The number of currencies has been successfully updated"},
        500: {"description": "Internal Server Error"},
    },
)
async def set_amount(
    set_amount_values: AmountSetSchema,
    currency_service: CurrencyServiceDep,
):
    """
    Устанавливает новые значения сумм для указанных валют.

    Обновляет суммы валют на основе предоставленных данных и возвращает подтверждение
    успешного обновления в формате, соответствующем OpenAPI.

    Args:
        set_amount_values (AmountSetSchema): Схема с новыми значениями сумм для валют.
        currency_service (CurrencyServiceDep): Зависимость сервиса валют для обработки запроса.

    Returns:
        AmountUpdateResponse: Объект с сообщением об успешном обновлении сумм валют.

    Raises:
        HTTPException: Если данные некорректны (status_code=422) или произошла внутренняя ошибка сервера (status_code=500).
    """
    currency_service.set_amount(set_amount=set_amount_values)
    return AmountUpdateResponse(
        detail="The number of currencies has been successfully updated"
    )


@router.post(
    path="/modify/",
    response_model=AmountUpdateResponse,
    summary="Изменение сумм валют",
    description="Изменяет суммы валют, добавляя или вычитая указанные значения.",
    responses={
        200: {"description": "The number of currencies has been successfully updated"},
        400: {"description": "The amount of currency cannot be less than zero: CODE"},
        500: {"description": "Internal Server Error"},
    },
)
async def modify_amount(
    update_amount: AmountUpdateSchema,
    currency_service: CurrencyServiceDep,
):
    """
    Изменяет суммы валют на основе предоставленных данных.

    Обновляет суммы валют, добавляя или вычитая указанные значения, и возвращает подтверждение
    успешного обновления в формате, соответствующем OpenAPI.

    Args:
        update_amount (AmountUpdateSchema): Схема с изменениями сумм для валют.
        currency_service (CurrencyServiceDep): Зависимость сервиса валют для обработки запроса.

    Returns:
        AmountUpdateResponse: Объект с сообщением об успешном обновлении сумм валют.

    Raises:
        HTTPException: Если данные некорректны (status_code=422) или произошла внутренняя ошибка сервера (status_code=500).
    """
    currency_service.modify_amount(modify_amount=update_amount)
    return AmountUpdateResponse(
        detail="The number of currencies has been successfully updated"
    )
