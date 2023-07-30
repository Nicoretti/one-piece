import os
import sys
from enum import IntEnum
from functools import (
    partial,
    wraps,
)
from typing import (
    Any,
    Callable,
    Mapping,
    Optional,
    Sequence,
)


class Console:
    stdout = partial(print, file=sys.stdout)
    stderr = partial(print, file=sys.stderr)


class ExitCode(IntEnum):
    SUCCESS = 0
    FAILURE = 1


def entry_point(*args, **kwargs) -> None:
    sys.exit(ExitCode.SUCCESS)


def _is_backtrace_enabled() -> bool:
    """Are stack traces enabled"""
    return os.environ.get("PYTHON_BACKTRACE", None) in ["1", "True", "true"]


def _disable_backtrace(func: Callable[..., None]) -> Callable[..., None]:
    """Decorator to suppress python stack traces"""

    @wraps(func)
    def catch_all(
            *args: Optional[Sequence[Any]], **kwargs: Optional[Mapping[Any, Any]]
    ) -> None:
        try:
            func(*args, **kwargs)
        except Exception as ex:
            msg = "\n".join(
                (
                    f"Error while executing [{__name__}], details: {str(ex) or '<not available>'}",
                    "To get a full stack trace set PYTHON_BACKTRACE=1",
                )
            )
            Console.stderr(msg)
            sys.exit(ExitCode.FAILURE)

    return catch_all


def main() -> None:
    _main: Callable[..., None] = (
        _disable_backtrace(entry_point) if not _is_backtrace_enabled() else entry_point  # type: ignore
    )
    _main()
