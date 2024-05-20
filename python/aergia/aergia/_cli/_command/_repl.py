from aergia._cli._command._utilities import default
from rich_argparse import ArgumentDefaultsRichHelpFormatter


def add_repl_subcommand(subparsers):
    subcommand = subparsers.add_parser(
        'repl',
        help='start repl client',
        formatter_class=ArgumentDefaultsRichHelpFormatter
    )
    subcommand.set_defaults(func=default)
    return subcommand
