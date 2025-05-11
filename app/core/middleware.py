import logging

from fastapi import FastAPI, Request, Response

from app.config import settings

logger = logging.getLogger(settings.logger.logger_name)


def register_middleware(app: FastAPI) -> None:
    @app.middleware("http")
    async def add_debug_logging(request: Request, call_next):
        logger.debug("Request: %s %s", request.method, request.url)

        response = await call_next(request)

        body_bytes = b""
        async for chunk in response.body_iterator:
            body_bytes += chunk

        try:
            body_text = body_bytes.decode()
        except UnicodeDecodeError:
            body_text = repr(body_bytes)

        logger.debug("Response: %s - %s", response.status_code, body_text)

        return Response(
            content=body_bytes,
            status_code=response.status_code,
            headers=dict(response.headers),
            media_type=response.media_type,
        )
