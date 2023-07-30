from rich.console import Console
from rich.theme import Theme

themes = Theme(
    {"info": "cyan", "warning": "yellow", "error": "red", "danger": "bold red"}
)

stdout = Console(theme=themes)
stderr = Console(theme=themes, stderr=True)


def command(*args) -> str:
    """Transform all args into a single command string"""
    args = (str(arg) for arg in args)
    return f"{' '.join(args)}"
