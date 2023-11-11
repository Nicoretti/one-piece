#!/usr/bin/env python3
import sys
import platform
import subprocess
from pathlib import Path


def _run(command, args):
    command = [command] + list(args)
    subprocess.run(command)


_COMMANDS = {
    'windows': 'start',
    'linux': 'xdg-open',
    'darwin': 'open',
}


def _windows(*args):
    command = _COMMANDS['windows']
    _run(command, args)


def _linux(*args):
    command = _COMMANDS['linux']
    _run(command, args)


def _mac(*args):
    command = _COMMANDS['darwin']
    _run(command, args)

def _os_name():
    return platform.system().lower()

def _is_command_available() -> bool:



def _launcher():
    launchers = {
        'windows': _windows,
        'linux': _linux,
        'darwin': _mac,
    }

    # add check if launcher is installed

    if (os_name := _os_name()) not in launchers:
        raise Exception(f"Platform {os_name} isn't supported")

    return launchers[os_name]


def main():
    try:
        print("Hello")
        launcher = _launcher()
        args = sys.argv[1:]
        launcher(*args)
    except Exception as ex:
        print(f"Error occurred, details {ex}", file=sys.stderr)
        print(f"Error occurred, details {ex}")
        logfile = Path().home() / "xopen.log"
        with open(logfile, 'w') as f:
            print(f"Error occurred, details {ex}", file=f)
        sys.exit(-1)


if __name__ == '__main__':
    main()
