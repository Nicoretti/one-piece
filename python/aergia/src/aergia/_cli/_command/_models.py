from rich.table import Table
from rich_argparse import ArgumentDefaultsRichHelpFormatter

from aergia._cli._command._utilities import ExitCode
from aergia._client import build_client


def models(settings, stdout, stderr):
    backend = settings["backend"]
    backend_settings = settings[backend]
    client = build_client(backend=backend, settings=backend_settings)
    models = client.models.list()

    table = Table(title="Available Models of Backend")
    table.add_column("Id/Name", justify="left", style="green")
    table.add_column("Owned By", justify="left", style="cyan")
    table.add_column("Created", justify="left", style="yellow")

    import datetime

    for m in models:
        created = f"{datetime.datetime.fromtimestamp(m.created)}"
        table.add_row(m.id, m.owned_by, created)

    stdout.print(table)

    return ExitCode.Success


def add_models_subcommand(subparsers):
    # fmt: off
    subcommand = subparsers.add_parser(
        "models",
        help="list available models of the backend",
        formatter_class=ArgumentDefaultsRichHelpFormatter,
    )
    subcommand.set_defaults(func=models)
    # fmt: on
    return subcommand
