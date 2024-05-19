import asyncio
import sys
import logging

from functools import wraps
from aergia._cli._parser import make_parser
from aergia._cli._output import stderr, stdout
from aergia._cli._command import ExitCode
from aergia._logging import logger
from rich.logging import RichHandler


def _protect(func, *args, **kwargs):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            exit_code = func(*args, **kwargs)
        except Exception as ex:
            err_msg = f"Error occurred, details: {ex}"
            logger.error(err_msg)
            stdout.print(err_msg, style='red')
            exit_code = ExitCode.Failure
        except asyncio.CancelledError as ex:
            err_msg = f"Canceled by user, details: {ex}"
            logger.error(err_msg)
            stdout.print(err_msg, style='red')
            exit_code = ExitCode.Failure
        return exit_code

    return wrapper


def main(argv=None):
    parser = make_parser()
    args = parser.parse_args(argv)

    if args.log_level:
        level = {
            'debug': logging.DEBUG,
            'info': logging.INFO,
            'warn': logging.WARN,
            'error': logging.ERROR,
            'critical': logging.CRITICAL
        }
        logging.basicConfig(
            level=level[args.log_level],
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            handlers=[RichHandler(console=stderr.stderr, rich_tracebacks=True)]
        )

    if not hasattr(args, "func"):
        parser.error("Subcommand required!")

    app = args.func if args.debug else _protect(args.func)
    exit_code = app(args, stdout, stderr)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
