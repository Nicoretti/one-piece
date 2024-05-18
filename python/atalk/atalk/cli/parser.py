import argparse
from atalk.cli.commands import default, chat, image, models
from rich_argparse import ArgumentDefaultsRichHelpFormatter
from contextlib import contextmanager


@contextmanager
def add_parser(subparsers, name, help):
    subparser = subparsers.add_parser(
        name,
        help=help,
        formatter_class=ArgumentDefaultsRichHelpFormatter
    )
    yield subparser


def create_parser():
    parser = argparse.ArgumentParser(prog='ai', formatter_class=ArgumentDefaultsRichHelpFormatter)
    parser.add_argument('--version', action='store_true', help='print the version')
    parser.add_argument('--debug', action='store_true', help='enable debug mode')
    parser.add_argument(
        '--log-level', default=None,
        choices=['debug', 'info', 'warn', 'error', 'critical'],
        help='Enable logger output'
    )

    subparsers = parser.add_subparsers(dest='subcommand')

    # chat command
    with add_parser(subparsers, 'chat', help='chat with the ai system') as p:
        p.add_argument('text', type=str, nargs=argparse.REMAINDER, help='Text input')
        p.add_argument('-r', '--role', type=str, help='Choose a role')
        p.add_argument('-s', '--session', nargs='?', const=True, help='Create or reuse a session')
        p.add_argument('-c', '--context', type=argparse.FileType('r'), help='File directory or stdin')
        p.add_argument(
            '-m', '--model',
            default='gpt-4o',
            choices=['gpt-4o', 'gpt-4', 'gpt-4-turbo', 'gpt-3.5-turbo'],
            help='Select a model'
        )
        p.add_argument('--stream', dest='stream', action='store_true', default=True, help='Enable streaming')
        p.set_defaults(func=chat)

    # tui subcommand
    tui_parser = subparsers.add_parser(
        'tui',
        help='start textul based tui client',
        formatter_class=ArgumentDefaultsRichHelpFormatter
    )
    tui_parser.set_defaults(func=default)

    # repl subcommand
    repl_parser = subparsers.add_parser(
        'repl',
        help='start repl client',
        formatter_class=ArgumentDefaultsRichHelpFormatter
    )
    repl_parser.set_defaults(func=default)

    # code subcommand
    code_parser = subparsers.add_parser(
        'code',
        help='Generate code',
        formatter_class=ArgumentDefaultsRichHelpFormatter
    )
    code_parser.set_defaults(func=default)
    code_parser.add_argument('text', type=str, nargs=argparse.REMAINDER, help='Code prompt')
    code_parser.add_argument('-r', '--role', type=str, help='Role to be used in addition')

    # image subcommand
    with add_parser(subparsers, 'image', help='Generate images') as p:
        p.add_argument('filename', type=str, help='Name of the imag for storage input')
        p.add_argument(
            '-m', '--model',
            choices=['dall-e-2', 'dall-e-3'],
            default='dall-e-2',
            help='Select a model'
        )
        p.add_argument('text', type=str, nargs=argparse.REMAINDER, help='Text input')
        p.set_defaults(func=image)

    # execute subcommand
    execute_parser = subparsers.add_parser(
        'execute',
        help='Generate and execute a command',
        formatter_class=ArgumentDefaultsRichHelpFormatter
    )
    execute_parser.set_defaults(func=default)
    execute_parser.add_argument('text', type=str, nargs=argparse.REMAINDER, help='Command prompt')
    execute_parser.add_argument('-s', '--shell', type=str, help='Specify the shell to be used for execution')
    execute_parser.add_argument('-r', '--role', type=str, help='Role to be taken into account')

    # sessions subcommand
    with add_parser(subparsers, 'session', help='Manage sessions') as p:
        p.set_defaults(func=default)
        sessions_subparsers = p.add_subparsers(dest='session_subcommand', help='Sessions commands')

        session_search_parser = sessions_subparsers.add_parser(
            'search',
            help='Search for text in sessions',
            formatter_class=ArgumentDefaultsRichHelpFormatter
        )
        session_search_parser.add_argument('text', type=str, help='Text to search')

        session_list_parser = sessions_subparsers.add_parser(
            'list',
            help='List all sessions',
            formatter_class=ArgumentDefaultsRichHelpFormatter
        )

        session_show_parser = sessions_subparsers.add_parser(
            'show',
            help='Show contents of a session',
            formatter_class=ArgumentDefaultsRichHelpFormatter
        )

        session_alias_parser = sessions_subparsers.add_parser(
            'alias',
            help='Alias for session command',
            formatter_class=ArgumentDefaultsRichHelpFormatter
        )

    # role subcommand
    role_parser = subparsers.add_parser('role', help='Manage roles')
    role_parser.set_defaults(func=default)
    role_subparsers = role_parser.add_subparsers(dest='role_subcommand', help='Roles commands')

    role_list_parser = role_subparsers.add_parser('list', help='List all roles')

    role_show_parser = role_subparsers.add_parser('show', help='Show a role')
    role_show_parser.add_argument('name', type=str, help='Role name')

    role_create_parser = role_subparsers.add_parser('create', help='Create a role')
    role_create_parser.add_argument('name', type=str, help='Role name')
    role_create_parser.add_argument('text', type=str, nargs='?', help='Role description')

    role_update_parser = role_subparsers.add_parser('update', help='Update a role')
    role_update_parser.add_argument('name', type=str, help='Role name')
    role_update_parser.add_argument('text', type=str, nargs='?', help='New role description')

    role_delete_parser = role_subparsers.add_parser('delete', help='Delete a role')
    role_delete_parser.add_argument('name', type=str, help='Role name')

    role_alias_parser = role_subparsers.add_parser('alias', help='Create an alias for a role')
    role_alias_parser.add_argument('role', type=str, help='Role name')
    role_alias_parser.add_argument('alias', type=str, help='Alias name')

    # info subcommand
    with add_parser(
            subparsers, 'info',
            help='Print info about data store and config file, etc.'
    ) as p:
        p.set_defaults(func=default)

    # models subcommand
    with add_parser(
            subparsers, 'models',
            help='List of all available models of the backend/service.'
    ) as p:
        p.set_defaults(func=models)

    return parser
