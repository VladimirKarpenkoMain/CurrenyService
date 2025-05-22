import argparse
from decimal import Decimal

from core.config import settings


def str2bool(v: str):
    """
    Преобразует строковое значение в булево.

    Функция принимает строку и возвращает True, если строка соответствует 'yes', 'true', 't' или '1',
    и False, если строка соответствует 'no', 'false', 'f' или '0'. В противном случае вызывает исключение.

    Args:
        v (str): Строковое значение для преобразования.

    Returns:
        bool: Булево значение, соответствующее входной строке.

    Raises:
        argparse.ArgumentTypeError: Если входная строка не соответствует ожидаемым булевым значениям.
    """
    if v.lower() in ("yes", "true", "t", "1"):
        return True
    elif v.lower() in ("no", "false", "f", "0"):
        return False
    else:
        raise argparse.ArgumentTypeError("Boolean value expected.")


def period_type(v: str):
    """
    Проверяет и преобразует строковое значение в положительное целое число.

    Функция преобразует строку в целое число и проверяет, что оно больше нуля.
    Если строка не является целым числом или число не положительное, вызывает исключение.

    Args:
        v (str): Строковое значение для преобразования.

    Returns:
        int: Положительное целое число.

    Raises:
        argparse.ArgumentTypeError: Если входная строка не является целым числом или число меньше либо равно нулю.
    """
    try:
        i_value = int(v)
    except ValueError:
        raise argparse.ArgumentTypeError("Integer value expected.")

    if i_value <= 0:
        raise argparse.ArgumentTypeError("Integer greater than 0 value expected.")

    return i_value


def parse_args() -> argparse.Namespace:
    """
    Парсит аргументы командной строки для сервиса валют.

    Функция создает парсер аргументов командной строки, добавляет обязательный аргумент периода
    в минутах, опциональный флаг режима отладки и аргументы для начальных сумм валют, указанных
    в конфигурации. Возвращает разобранные аргументы.
    """
    parser = argparse.ArgumentParser(description="Currency Service")
    parser.add_argument(
        "--period",
        type=period_type,
        required=True,
        help="Fetch period in minutes",
    )
    parser.add_argument(
        "--debug",
        type=str2bool,
        default=False,
        help="Debug mode",
    )

    for currency in settings.currencies:
        parser.add_argument(
            f"--{currency}",
            type=Decimal,
            default=0.0,
            help=f"Initial {currency} amount",
        )

    args = parser.parse_args()
    return args
