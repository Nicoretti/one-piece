import asyncio
import logging
import sys
from functools import wraps

from rich.logging import RichHandler

from aergia._cli._command._parser import make_parser
from aergia._cli._command._utilities import ExitCode
from aergia._cli._io import stderr, stdout
from aergia._config._settings import DEFAULT_CONFIG, settings_from
from aergia._logging import logger


def _protect(func, *args, **kwargs):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            exit_code = func(*args, **kwargs)
        except Exception as ex:
            err_msg = f"Error occurred, details: {ex}"
            logger.error(err_msg)
            stdout.print(err_msg, style="red")
            exit_code = ExitCode.Failure
        except asyncio.CancelledError as ex:
            err_msg = f"Canceled by user, details: {ex}"
            logger.error(err_msg)
            stdout.print(err_msg, style="red")
            exit_code = ExitCode.Failure
        return exit_code

    return wrapper


def main(argv=None):
    parser = make_parser()
    args = parser.parse_args(argv)

    levels = {
        "debug": logging.DEBUG,
        "info": logging.INFO,
        "warn": logging.WARN,
        "error": logging.ERROR,
        "critical": logging.CRITICAL,
    }
    level = args.log_level or "error"
    logging.basicConfig(
        level=levels[level],
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[RichHandler(console=stderr, rich_tracebacks=True)],
    )

    if not hasattr(args, "func"):
        parser.error("Subcommand required!")

    settings = settings_from(args, DEFAULT_CONFIG)
    app = args.func if args.debug else _protect(args.func)
    exit_code = app(settings, stdout, stderr)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
