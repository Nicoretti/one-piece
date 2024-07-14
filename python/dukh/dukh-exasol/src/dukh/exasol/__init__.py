from collections import defaultdict

from exasol.bucketfs import Service
from invoke import Collection, task
from rich.tree import Tree


from rich.console import Console
from rich.theme import Theme

themes = Theme(
    {"info": "cyan", "warning": "yellow", "error": "red", "danger": "bold red"}
)

stdout = Console(theme=themes)


@task
def buckets(
    _context, host="http://127.0.0.1", port=6666, username="w", password="write"
):
    """
    List all buckets of a specific bucketfs service

    Args:
        host: (default: 'http://127.0.0.1')
        port: (default: 6666)
        username: (default: 'w')
        password: (default: 'write')
    """
    credentials = defaultdict(lambda: {"username": username, "password": password})
    bucketfs = Service(f"{host}:{port}", credentials)
    tree = Tree(f"🌐 Bucketfs", style="Red")
    try:
        for bucket in bucketfs:
            child = tree.add(f"💾 {bucket}", style="cyan")
            for f in bucketfs[bucket].files:
                child.add(f"📄 {f}", style="green")
    except Exception as ex:
        stdout.print(f"Couldn't list bucket, details: {ex}")
    stdout.print(tree)


ns = Collection('exasol')
ns.add_task(buckets, name='bfs')
