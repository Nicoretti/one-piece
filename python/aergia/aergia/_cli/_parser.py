import argparse
from aergia._cli._command import default, chat, image, models
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


def add_chat_subcommand(subparsers):
    subcommand = subparsers.add_parser(
        'chat',
        help='chat with the ai system',
        formatter_class=ArgumentDefaultsRichHelpFormatter
    )
    subcommand.add_argument(
        'text', type=str, nargs=argparse.REMAINDER, help='Text input'
    )
    subcommand.add_argument(
        '-r', '--role', type=str, help='Choose a role'
    )
    subcommand.add_argument(
        '-s', '--session', nargs='?', const=True, help='Create or reuse a session'
    )
    subcommand.add_argument(
        '-c', '--context', type=argparse.FileType('r'), help='File directory or stdin'
    )
    subcommand.add_argument(
        '-m', '--model',
        default='gpt-4o',
        choices=['gpt-4o', 'gpt-4', 'gpt-4-turbo', 'gpt-3.5-turbo'],
        help='Select a model'
    )
    subcommand.add_argument(
        '--stream', dest='stream', action='store_true', default=True, help='Enable streaming'
    )
    subcommand.set_defaults(func=chat)
    return subcommand


def add_tui_subcommand(subparsers):
    subcommand = subparsers.add_parser(
        'tui',
        help='start textul based tui client',
        formatter_class=ArgumentDefaultsRichHelpFormatter
    )
    subcommand.set_defaults(func=default)
    return subcommand


def add_repl_subcommand(subparsers):
    subcommand = subparsers.add_parser(
        'repl',
        help='start repl client',
        formatter_class=ArgumentDefaultsRichHelpFormatter
    )
    subcommand.set_defaults(func=default)
    return subcommand


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


def add_image_subcommand(subparsers):
    subcommand = subparsers.add_parser(
        'image',
        help='generate images',
        formatter_class=ArgumentDefaultsRichHelpFormatter
    )
    subcommand.add_argument(
        'filename', type=str, help='Name of the imag for storage input'
    )
    subcommand.add_argument(
        '-m', '--model',
        default='dall-e-2',
        choices=['dall-e-2', 'dall-e-3'],
        help='Select a model'
    )
    subcommand.add_argument(
        'text', type=str, nargs=argparse.REMAINDER, help='Text input'
    )
    subcommand.set_defaults(func=image)
    return subcommand


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


def add_session_subcommand(subparsers):
    subcommand = subparsers.add_parser(
        'session',
        help='Manage sessions',
        formatter_class=ArgumentDefaultsRichHelpFormatter
    )
    subcommand.set_defaults(func=default)

    sub_subparsers = subcommand.add_subparsers(
        dest='session_subcommand', help='Sessions commands'
    )

    search_command = sub_subparsers.add_parser(
        'search',
        help='Search for text in sessions',
        formatter_class=ArgumentDefaultsRichHelpFormatter
    )
    search_command.add_argument('text', type=str, help='Text to search')

    list_command = sub_subparsers.add_parser(
        'list',
        help='List all sessions',
        formatter_class=ArgumentDefaultsRichHelpFormatter
    )

    show_command = sub_subparsers.add_parser(
        'show',
        help='Show contents of a session',
        formatter_class=ArgumentDefaultsRichHelpFormatter
    )

    alias_command = sub_subparsers.add_parser(
        'alias',
        help='Alias for session command',
        formatter_class=ArgumentDefaultsRichHelpFormatter
    )
    return subcommand


def add_role_subcommand(subparsers):
    subcommand = subparsers.add_parser(
        'role',
        help='Manage roles',
        formatter_class=ArgumentDefaultsRichHelpFormatter
    )
    subcommand.set_defaults(func=default)

    sub_subparsers = subcommand.add_subparsers(
        dest='role_subcommand', help='Roles commands'
    )

    list_command = sub_subparsers.add_parser(
        'list', help='List all roles'
    )

    show_command = sub_subparsers.add_parser(
        'show', help='Show a role'
    )
    show_command.add_argument(
        'name', type=str, help='Role name'
    )

    create_command = sub_subparsers.add_parser(
        'create', help='Create a role'
    )
    create_command.add_argument(
        'name', type=str, help='Role name'
    )
    create_command.add_argument(
        'text', type=str, nargs='?', help='Role description'
    )

    update_command = sub_subparsers.add_parser(
        'update', help='Update a role'
    )
    update_command.add_argument(
        'name', type=str, help='Role name'
    )
    update_command.add_argument(
        'text', type=str, nargs='?', help='New role description'
    )

    delete_command = sub_subparsers.add_parser(
        'delete', help='Delete a role'
    )
    delete_command.add_argument(
        'name', type=str, help='Role name'
    )

    alias_command = sub_subparsers.add_parser(
        'alias', help='Create an alias for a role'
    )
    alias_command.add_argument(
        'role', type=str, help='Role name'
    )
    alias_command.add_argument(
        'alias', type=str, help='Alias name'
    )
    return subcommand


def add_info_subcommand(subparsers):
    subcommand = subparsers.add_parser(
        subparsers, 'info',
        help='Print info about data store and config file, etc.',
        formatter_class=ArgumentDefaultsRichHelpFormatter
    )
    subcommand.set_defaults(func=default)
    return subcommand


def add_models_subcommand(subparsers):
    subcommand = subparsers.add_parser(
        'models',
        help='list available models of the backend',
        formatter_class=ArgumentDefaultsRichHelpFormatter
    )
    subcommand.set_defaults(func=models)
    return subcommand


def make_parser():
    parser = argparse.ArgumentParser(
        prog='ae[rgia]', formatter_class=ArgumentDefaultsRichHelpFormatter
    )
    parser.add_argument(
        '--version', action='store_true', help='print the version'
    )
    parser.add_argument(
        '--debug', action='store_true', help='enable debug mode'
    )
    parser.add_argument(
        '--log-level', default=None,
        choices=['debug', 'info', 'warn', 'error', 'critical'],
        help='configure the log-level of the application'
    )

    subparsers = parser.add_subparsers(dest='subcommand')

    add_chat_subcommand(subparsers)
    # add_tui_subcommand(subparsers)
    # add_repl_subcommand(subparsers)
    # add_code_subcommand(subparsers)
    add_image_subcommand(subparsers)
    # add_execute_subcommand(subparsers)
    # add_session_subcommand(subparsers)
    # add_role_subcommand(subparsers)
    # add_info_subcommand(subparsers)
    add_models_subcommand(subparsers)

    return parser
