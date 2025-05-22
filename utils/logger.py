import logging

from app.config import settings

formatter = logging.Formatter(
    fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

def setup_logging(debug: bool):
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
