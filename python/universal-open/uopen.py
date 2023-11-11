#!/usr/bin/env python3
import sys
import platform
import subprocess
import shutil
from enum import IntEnum
from argparse import ArgumentParser


def _is_command_available(command) -> bool:
    command = shutil.which(command)
    return not (command is None or command == '')


def _run(command, *args):
    command = [command]
    command.extend(args)
    subprocess.run(command)


def _launcher():
    os_name = platform.system().lower()
    launchers = {
        'windows': 'start',
        'linux': 'xdg-open',
        'darwin': 'open',
    }

    if os_name not in launchers:
        raise Exception(f"Platform <{os_name}> isn't supported yet.")

    launcher = launchers[os_name]
    if not _is_command_available(launcher):
        raise Exception(f"The required launcher command <{launcher}>, is not available!")

    def application_launcher(*args):
        _run(launcher, *args)

    return application_launcher


def _parser():
    parser = ArgumentParser("uopen", description='Universal open ')
    parser.add_argument(
        'arguments', metavar='{ file | URL }', nargs='*', help='File or URL to open.'
    )
    return parser


class ExitCode(IntEnum):
    SUCCESS = 0
    FAILURE = -1


def entry_point(argv=None) -> ExitCode:
    args = _parser().parse_args(argv)
    try:
        launcher = _launcher()
        launcher(*args.arguments)
    except Exception as ex:
        print(ex, file=sys.stderr)
        return ExitCode.FAILURE
    return ExitCode.SUCCESS


def main(argv=None):
    sys.exit(entry_point(argv))


if __name__ == '__main__':
    main()
