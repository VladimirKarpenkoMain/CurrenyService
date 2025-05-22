import logging

from fastapi import FastAPI, Request, Response

from core.config import settings

logger = logging.getLogger(settings.logger.logger_name)


def register_middleware(app: FastAPI) -> None:
    """
    Регистрирует middleware для FastAPI приложения, который логирует запросы и ответы для отладки.

    :param app: Экземпляр FastAPI приложения.
    """

    @app.middleware("http")
    async def add_debug_logging(request: Request, call_next):
        """
        Middleware для логирования запросов и ответов.

        :param request: Входящий HTTP-запрос.
        :param call_next: Функция для вызова следующего обработчика.
        :return: HTTP-ответ.
        """
        try:
            request_body = await request.json()
        except Exception:
            request_body = None
        logger.debug(
            "Request: %s %s body: %s", request.method, request.url, request_body
        )

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
