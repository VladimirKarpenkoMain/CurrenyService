import argparse

from app.config import settings


def parse_debug(val: str) -> bool:
    truthy = {"1", "true", "True", "y", "Y"}
    falsy = {"0", "false", "False", "n", "N"}
    if val in truthy:
        return True
    if val in falsy:
        return False
    raise ValueError(f"Invalid debug value: {val}")


def parse_args():
    parser = argparse.ArgumentParser(description="Currency Service")
    parser.add_argument(
        "--period",
        type=int,
        required=True,
        help="Fetch period in minutes",
    )
    parser.add_argument(
        "--debug",
        type=str,
        default="false",
        help="Debug mode",
    )
    for currency in settings.currencies:
        parser.add_argument(
            f"--{currency}",
            type=float,
            default=0.0,
            help=f"Initial {currency} amount",
        )
    args = parser.parse_args()
    args.debug = parse_debug(args.debug)
    return args
