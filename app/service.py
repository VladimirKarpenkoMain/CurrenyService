import asyncio
import logging

import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI

from .api import api_router
from .config import settings
from .utils.logger import setup_logging
from .utils.cli import parse_args
from .core.state import currency_state
from .core.scheduler import scheduler_fetch, scheduler_print
from .core.middleware import register_middleware

logger = logging.getLogger(settings.logger.logger_name)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("App started")
    yield
    logger.info("App finished")


app = FastAPI(lifespan=lifespan)
app.include_router(api_router)


async def main():
    args = parse_args()

    setup_logging(args.debug)

    if args.debug:
        register_middleware(app)

    init_state = {}
    for currency in settings.currencies:
        attr = getattr(args, currency)
        init_state[currency.upper()] = attr

    currency_state.init_amount(amounts=init_state)

    server_config = uvicorn.Config(
        app,
        host=settings.run.host,
        port=settings.run.port,
        workers=settings.run.count_workers,
    )
    server = uvicorn.Server(server_config)

    tasks = [
        scheduler_fetch(state=currency_state, period=args.period),
        scheduler_print(),
        server.serve(),
    ]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
