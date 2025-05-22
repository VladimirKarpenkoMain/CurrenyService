from fastapi import APIRouter
from app.api.v1.currency import router as currency_router

v1_router = APIRouter(prefix="/v1", tags=["v1"])

v1_router.include_router(router=currency_router)
