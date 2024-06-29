from rich_argparse import ArgumentDefaultsRichHelpFormatter

from aergia._cli._command._utilities import default


def add_info_subcommand(subparsers):
    # fmt: off
    subcommand = subparsers.add_parser(
        subparsers,
        "info",
        help="Print info about data store and config file, etc.",
        formatter_class=ArgumentDefaultsRichHelpFormatter,
    )
    subcommand.set_defaults(func=default)
    # fmt: on
    return subcommand
