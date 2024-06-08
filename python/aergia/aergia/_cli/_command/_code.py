import argparse
from aergia._cli._command._utilities import default
from rich_argparse import ArgumentDefaultsRichHelpFormatter


def add_code_subcommand(subparsers):
    subcommand = subparsers.add_parser(
        'code',
        help='Generate code',
        formatter_class=ArgumentDefaultsRichHelpFormatter
    )
    subcommand.add_argument(
        'text', type=str, nargs=argparse.REMAINDER, help='Code prompt'
    )
    subcommand.add_argument(
        '-r', '--role', type=str, help='Role to be used in addition'
    )
    subcommand.set_defaults(func=default)
    return subcommand
