import json
from pathlib import Path

from rich.json import JSON
from rich.syntax import Syntax
from rich.table import Table
from rich_argparse import ArgumentDefaultsRichHelpFormatter

from aergia._cli._command._utilities import ExitCode
from aergia._roles import create_env, load


def list_roles(settings, stdout, stderr):
    table = Table(title="Available Roles")
    table.add_column("Role", justify="left", style="green")
    table.add_column("Description", justify="left", style="cyan")

    paths = None
    env = create_env(paths=paths)
    roles = env.list_templates(extensions="role")
    for role in roles:
        name = role.split(".")[0]
        template, metadata = load(name)
        table.add_row(name, metadata["description"] if "description" in metadata else "")

    stdout.print(table)

    return ExitCode.Success


def show_role(settings, stdout, stderr):
    name = settings["name"]
    table = Table(title=f"{name}")
    table.add_column("Definition", justify="left")
    table.add_column("Metadata", justify="left", style="cyan")

    template, metadata = load(settings["name"])

    content = Path(template.filename).read_text()
    table.add_row(Syntax(content, "jinja"), JSON(json.dumps(metadata)))

    stdout.print(table)

    return ExitCode.Success


def add_role_subcommand(subparsers):
    # fmt: off
    subcommand = subparsers.add_parser(
        "role", help="Manage roles", formatter_class=ArgumentDefaultsRichHelpFormatter
    )

    sub_subparsers = subcommand.add_subparsers(
        dest="role_subcommand", help="Roles commands"
    )

    list_command = sub_subparsers.add_parser(
        "list",
        help="List all roles",
        formatter_class=ArgumentDefaultsRichHelpFormatter
    )
    list_command.set_defaults(func=list_roles)

    show_command = sub_subparsers.add_parser(
        "show",
        help="Show a role",
        formatter_class=ArgumentDefaultsRichHelpFormatter
    )
    show_command.add_argument("name", type=str, help="Role name")
    show_command.set_defaults(func=show_role)

    # create_command = sub_subparsers.add_parser("create", help="Create a role")
    # create_command.add_argument("name", type=str, help="Role name")
    # create_command.add_argument("text", type=str, nargs="?", help="Role description")

    # update_command = sub_subparsers.add_parser("update", help="Update a role")
    # update_command.add_argument("name", type=str, help="Role name")
    # update_command.add_argument(
    #     "text", type=str, nargs="?", help="New role description"
    # )

    # delete_command = sub_subparsers.add_parser("delete", help="Delete a role")
    # delete_command.add_argument("name", type=str, help="Role name")

    # alias_command = sub_subparsers.add_parser(
    #     "alias", help="Create an alias for a role"
    # )
    # alias_command.add_argument("role", type=str, help="Role name")
    # alias_command.add_argument("alias", type=str, help="Alias name")

    # fmt: on
    return subcommand
