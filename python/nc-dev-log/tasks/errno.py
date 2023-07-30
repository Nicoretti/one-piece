import errno
import os

from invoke import Collection, task
from rich.table import Table

from tasks.terminal import stdout


@task(iterable=["id", "code"])
def explain(_context, id: None, code=None):
    """
    Lists detailed errno information based on the code or id.

    By default it will list all errno information on the system its running on.

    Args:
        id: errno error id
        code: errno error code

    Examples:
        inv errno
        inv errno --id 11
        inv errno --code ERFKILL
    """
    id = [int(id, 0) for id in id] if id else None

    def _filter(ids, code):
        if not ids and not code:
            return lambda e: True
        return lambda e: e[0] in ids or e[1] in code

    table = Table(title="Errno codes")
    table.add_column("Id", justify="right", style="red")
    table.add_column("Code", style="cyan")
    table.add_column("Description", style="green")

    error_codes = filter(_filter(id, code), errno.errorcode.items())
    for id, code in sorted(error_codes):
        table.add_row(f"{id}", code, os.strerror(id))

    stdout.print(table)


namespace = Collection()
namespace.add_task(explain)
