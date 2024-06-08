from aergia._cli._command._utilities import default
from rich_argparse import ArgumentDefaultsRichHelpFormatter


def add_info_subcommand(subparsers):
    subcommand = subparsers.add_parser(
        subparsers, 'info',
        help='Print info about data store and config file, etc.',
        formatter_class=ArgumentDefaultsRichHelpFormatter
    )
    subcommand.set_defaults(func=default)
    return subcommand
