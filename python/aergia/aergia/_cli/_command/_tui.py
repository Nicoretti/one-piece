from aergia._cli._command._utilities import default
from rich_argparse import ArgumentDefaultsRichHelpFormatter


def add_tui_subcommand(subparsers):
    subcommand = subparsers.add_parser(
        'tui',
        help='start textul based tui client',
        formatter_class=ArgumentDefaultsRichHelpFormatter
    )
    subcommand.set_defaults(func=default)
    return subcommand
