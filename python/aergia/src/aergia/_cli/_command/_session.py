from rich.markdown import Markdown
from rich.table import Table
from rich_argparse import ArgumentDefaultsRichHelpFormatter

from aergia._cli._command._utilities import ExitCode
from aergia._model._data import Message, Session
from aergia._model._load import load, load_list
from aergia._model._storage import application_db


def list_sessions(settings, stdout, stderr):
    table = Table(title="Chat Sessions")
    table.add_column("Id", justify="right")
    table.add_column("Name", justify="left", style="green")
    table.add_column("Model", justify="left", style="cyan")
    table.add_column("Created", justify="left", style="yellow")

    db = application_db()
    limit = None if settings["all"] else settings["limit"]
    sessions = load_list(Session, db, limit=limit, offset=settings["offset"])
    for s in sessions:
        table.add_row(
            f"{s.id}",
            s.name,
            s.model,
            f"{s.created}",
        )

    stdout.print(table)

    return ExitCode.Success


def show_session(settings, stdout, stderr):
    from rich.panel import Panel

    db = application_db()
    messages = list(load(Message, key="session_id", value=settings["id"], db=db))
    for m in messages:
        color = "blue" if m.role == "user" else "magenta"
        p = Panel(Markdown(m.content), title=m.role, style=color)
        stdout.print(p)

    return ExitCode.Success


def add_session_subcommand(subparsers):
    # fmt: off
    subcommand = subparsers.add_parser(
        "session",
        help="manage sessions",
        formatter_class=ArgumentDefaultsRichHelpFormatter,
    )

    sub_subparsers = subcommand.add_subparsers(
        dest="session_subcommand", help="Sessions commands"
    )

    list_command = sub_subparsers.add_parser(
        "list",
        help="list all sessions",
        formatter_class=ArgumentDefaultsRichHelpFormatter,
    )
    list_command.add_argument(
        "-a", "--all", action="store_true", default=False, help="list all images"
    )
    list_command.add_argument(
        "-l", "--limit", type=int, default=10, help="amount of images to list"
    )
    list_command.add_argument(
        "-o", "--offset", type=int, default=0, help="offset for listing images"
    )
    list_command.set_defaults(func=list_sessions)

    show_command = sub_subparsers.add_parser(
        "show",
        help="show contents of a session",
        formatter_class=ArgumentDefaultsRichHelpFormatter,
    )
    show_command.add_argument("id", type=int, help="session id of session to show")
    show_command.set_defaults(func=show_session)
    # fmt: on
    return subcommand
