from typing import Any

from rich.console import Console

stdout = Console()
stderr = Console(stderr=True)


def command(*args: Any) -> str:
    """Transform all args into a single command string"""
    arguments = (str(arg) for arg in args)
    return f"{' '.join(arguments)}"
