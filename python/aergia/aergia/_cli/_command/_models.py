import os
from aergia._cli._command._utilities import ExitCode
from openai import OpenAI
from rich.table import Table
from rich_argparse import ArgumentDefaultsRichHelpFormatter


def models(args, stdout, stderr):
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY")
    )
    models = client.models.list()

    table = Table(title='Available Models of Backend')
    table.add_column("Id/Name", justify='left', style='green')
    table.add_column("Owned By", justify='left', style='cyan')
    table.add_column("Created", justify='left', style='yellow')

    import datetime
    for m in models:
        created = f"{datetime.datetime.fromtimestamp(m.created)}"
        table.add_row(m.id, m.owned_by, created)

    stdout.print(table)

    return ExitCode.Success


def add_models_subcommand(subparsers):
    subcommand = subparsers.add_parser(
        'models',
        help='list available models of the backend',
        formatter_class=ArgumentDefaultsRichHelpFormatter
    )
    subcommand.set_defaults(func=models)
    return subcommand
