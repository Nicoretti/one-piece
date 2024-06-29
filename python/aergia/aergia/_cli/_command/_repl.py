from rich_argparse import ArgumentDefaultsRichHelpFormatter

from aergia._cli._command._utilities import default


def add_repl_subcommand(subparsers):
    subcommand = subparsers.add_parser(
        "repl",
        help="start repl client",
        formatter_class=ArgumentDefaultsRichHelpFormatter,
    )
    subcommand.set_defaults(func=default)
    return subcommand
