from rich_argparse import ArgumentDefaultsRichHelpFormatter

from aergia._cli._command._utilities import default


def add_tui_subcommand(subparsers):
    # fmt: off
    subcommand = subparsers.add_parser(
        "tui",
        help="start textul based tui client",
        formatter_class=ArgumentDefaultsRichHelpFormatter,
    )
    subcommand.set_defaults(func=default)
    # fmt: on
    return subcommand
