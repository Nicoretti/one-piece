from aergia._cli._command._utilities import default
from rich_argparse import ArgumentDefaultsRichHelpFormatter


def add_session_subcommand(subparsers):
    subcommand = subparsers.add_parser(
        'session',
        help='Manage sessions',
        formatter_class=ArgumentDefaultsRichHelpFormatter
    )
    subcommand.set_defaults(func=default)

    sub_subparsers = subcommand.add_subparsers(
        dest='session_subcommand', help='Sessions commands'
    )

    search_command = sub_subparsers.add_parser(
        'search',
        help='Search for text in sessions',
        formatter_class=ArgumentDefaultsRichHelpFormatter
    )
    search_command.add_argument('text', type=str, help='Text to search')

    list_command = sub_subparsers.add_parser(
        'list',
        help='List all sessions',
        formatter_class=ArgumentDefaultsRichHelpFormatter
    )

    show_command = sub_subparsers.add_parser(
        'show',
        help='Show contents of a session',
        formatter_class=ArgumentDefaultsRichHelpFormatter
    )

    alias_command = sub_subparsers.add_parser(
        'alias',
        help='Alias for session command',
        formatter_class=ArgumentDefaultsRichHelpFormatter
    )
    return subcommand
