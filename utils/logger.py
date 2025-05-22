import logging

from core.config import settings

formatter = logging.Formatter(
    fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def setup_logging(debug: bool):
    """
    Настраивает логирование для приложения с использованием консольного и файлового обработчиков.

    Эта функция настраивает логгер с именем, указанным в конфигурации настроек.
    Логгер настроен для вывода логов как в консоль, так и в файл, с уровнем логирования,
    определяемым параметром `debug`. Формат логов включает временную метку, имя логгера,
    уровень логирования и сообщение.

    Args:
        debug (bool): Если True, устанавливает уровень логирования на DEBUG; в противном случае — на INFO.

    Returns:
        None
    """
    logger = logging.getLogger(settings.logger.logger_name)
    logger.setLevel(logging.DEBUG if debug else logging.INFO)

    console_handler = logging.StreamHandler()
    file_handler = logging.FileHandler(
        settings.logger.log_file,
        encoding="utf-8",
    )

    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
