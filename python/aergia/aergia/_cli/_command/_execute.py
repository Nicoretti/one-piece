import argparse
from aergia._cli._command._utilities import default
from rich_argparse import ArgumentDefaultsRichHelpFormatter


def add_execute_subcommand(subparsers):
    subcommand = subparsers.add_parser(
        'execute',
        help='Generate and execute a command',
        formatter_class=ArgumentDefaultsRichHelpFormatter
    )
    subcommand.add_argument(
        'text', type=str, nargs=argparse.REMAINDER, help='Command prompt'
    )
    subcommand.add_argument(
        '-s', '--shell', type=str, help='Specify the shell to be used for execution'
    )
    subcommand.add_argument(
        '-r', '--role', type=str, help='Role to be taken into account'
    )
    subcommand.set_defaults(func=default)
    return subcommand
