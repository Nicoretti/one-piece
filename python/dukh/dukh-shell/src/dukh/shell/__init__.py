import os
from collections import Counter

from invoke import Collection, task
from rich.table import Table
from rich.theme import Theme
from rich.console import Console

themes = Theme(
    {"info": "cyan", "warning": "yellow", "error": "red", "danger": "bold red"}
)

stdout = Console(theme=themes)
stderr = Console(theme=themes, stderr=True)


@task
def env(_context, table=True):
    """
    List all environment variables and their values.

    Args:
        table: whether nor not to format it as table (default: true).
    """

    def raw(e):
        for name, value in e.items():
            yield f"{name}: {value}"

    def table_based(e):
        table = Table(title="Environment Variables", highlight=True)
        table.add_column("Name", justify="left")
        table.add_column("Value")
        for name, value in e.items():
            table.add_row(f"{name}", value)
        yield table

    output = table_based if table else raw
    for e in output(os.environ):
        stdout.print(e)


@task
def path(_context, warnings=True):
    """
    List all paths within the PATH variable.

    Args:
        warnings: warn if a path is contained multiple times within the PATH variable
                  (default: true).
    """
    paths = os.environ["PATH"].split(":")
    duplicates = (
        (p for p, count in Counter(paths).items() if count > 1) if warnings else []
    )
    for p in duplicates:
        stderr.print(f"Warning: found duplicates of {p} in PATH", style="warning")
    deduplicated_paths = dict().fromkeys(paths)
    for p in deduplicated_paths:
        stdout.print(p)


ns = Collection("shell")
ns.add_task(env, "env")
ns.add_task(path)
