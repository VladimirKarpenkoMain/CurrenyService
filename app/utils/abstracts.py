from abc import abstractmethod, ABC

from app.schemas.currency import AmountUpdateSchema


class AbstractFetchService(ABC):
    @abstractmethod
    async def fetch_rates(self):
        pass


class AbstractCurrencyService(ABC):
    @abstractmethod
    async def get_by_code(self, currency_code: str):
        pass

    @abstractmethod
    async def set_amount(self, set_amount: AmountUpdateSchema):
        pass

    @abstractmethod
    async def modify_amount(self, modify_amount: AmountUpdateSchema):
        pass

    @abstractmethod
    async def get_total_info(self):
        pass
