from aergia._cli._command._utilities import default
from rich_argparse import ArgumentDefaultsRichHelpFormatter


def add_role_subcommand(subparsers):
    subcommand = subparsers.add_parser(
        'role',
        help='Manage roles',
        formatter_class=ArgumentDefaultsRichHelpFormatter
    )
    subcommand.set_defaults(func=default)

    sub_subparsers = subcommand.add_subparsers(
        dest='role_subcommand', help='Roles commands'
    )

    list_command = sub_subparsers.add_parser(
        'list', help='List all roles'
    )

    show_command = sub_subparsers.add_parser(
        'show', help='Show a role'
    )
    show_command.add_argument(
        'name', type=str, help='Role name'
    )

    create_command = sub_subparsers.add_parser(
        'create', help='Create a role'
    )
    create_command.add_argument(
        'name', type=str, help='Role name'
    )
    create_command.add_argument(
        'text', type=str, nargs='?', help='Role description'
    )

    update_command = sub_subparsers.add_parser(
        'update', help='Update a role'
    )
    update_command.add_argument(
        'name', type=str, help='Role name'
    )
    update_command.add_argument(
        'text', type=str, nargs='?', help='New role description'
    )

    delete_command = sub_subparsers.add_parser(
        'delete', help='Delete a role'
    )
    delete_command.add_argument(
        'name', type=str, help='Role name'
    )

    alias_command = sub_subparsers.add_parser(
        'alias', help='Create an alias for a role'
    )
    alias_command.add_argument(
        'role', type=str, help='Role name'
    )
    alias_command.add_argument(
        'alias', type=str, help='Alias name'
    )
    return subcommand
