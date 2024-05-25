from __future__ import annotations
import os
import tomli
from typing import Generic, TypeVar
from collections import ChainMap
from dataclasses import dataclass
from pathlib import Path
from inspect import cleandoc


def default_config():
    DEFAULT_CONFIG = cleandoc("""
    [defaults]
    db_name = "aergia"  # base name of the database which will be used to store chats, images, etc.
    backend="openai"    # backend which should be used by default

    [backends.openai]
    name = "openai"                         # name of the backend
    base_url = "https://api.openai.com/v1"  # base url of the backend api
    token=""                                # token used to authenticate against the backend

    [commands.image]
    generate.model = "dall-e-3" # default model to use
    generate.name = "unnamed"   # default name to use if none is specified
    list.all = false            # should all images be listed if true, limit will be ignored
    list.limit = 10             # amount of images which should be listed by default
    list.offset = 0             # offset from which the images should be started to be listed

    [commands.chat]
    model = "gpt-4o"
    # role = None               # role which should be used by default (if set session will be ignoed)
    # session = None            # session which should be used by default (conflicts with role)
    # context = None            # context file which should be passed as context

    # [commands.models]
    # currently does not have any associated settings
    """)
    config = tomli.loads(DEFAULT_CONFIG)
    config['commands']['chat']['role'] = None
    config['commands']['chat']['session'] = None
    config['commands']['chat']['context'] = None
    config['commands']['models'] = {}
    return config


def load_config_file(path: Path):
    with open(path, 'rb') as f:
        return tomli.load(f)


def user_config(cfg: Path):
    if not cfg.exists():
        return {}
    return load_config_file(cfg)


def env_config(env):
    def commands_env():
        cfg = {}
        return cfg

    def defaults():
        cfg = {}
        return cfg

    def openai_env():
        cfg = {}
        settings = {
            "OPENAI_API_KEY": "token",
            "OPENAI_BASE_URL": "base_url",
        }
        settings_in_env = {k: v for k, v in settings.items() if k in env}
        for env_name, cfg_name in settings_in_env.items():
            cfg[cfg_name] = env[env_name]

        if len(cfg) > 0:
            cfg['name'] = 'openai'
        return cfg

    config = {
        "defaults": {"defaults": defaults()},
        "backends": {"openai": openai_env()},
        "commands": {"commands": commands_env()},
    }

    return config


def command_line(arguments):
    command = arguments.subcommand
    config = {'defaults': {'db_name': 'aergia', 'backend': 'openai'}}

    def chat_args(args):
        return {'chat': {'model': args.model}}

    def image_args(args):
        match args.subcommand:
            case "generate":
                return {
                    "model": args.model,
                    "name": args.name
                }
            case "list":
                return {
                    "all": args.all,
                    "limit": args.limit,
                    "offset": args.offset
                }
            case _:
                return {}

    dispatcher = {
        'chat': chat_args,
        'image': image_args,
    }
    try:
        config[command] = dispatcher[command](arguments)
    except KeyError:
        config[command] = {}

    return config


class Settings:

    def __init__(self, args, env=None, cfg=None, defaults=None):
        env = env or os.environ.copy()
        cfg = cfg or (Path.home() / "aergia.toml")
        self._settings = ChainMap(
            command_line(args),
            env_config(env),
            user_config(cfg),
            defaults or default_config()
        )

    def __getattr__(self, name):
        try:
            return self._settings[name]
        except KeyError:
            raise AttributeError(f"'Settings' object has no attribute '{name}'")


#
# @dataclass(frozen=True)
# class Namespace(Generic[T]):
#    prefix: str
#
T = TypeVar("T")


@dataclass(frozen=True)
class Setting(Generic[T]):
    name: str
    type: T
    default: T | None
    description: str = ""


@dataclass(frozen=True)
class Namespace(Generic[T]):
    name: str
    settings: list
    description: str = ""

    def add_setting(self):
        pass

    def add_namespace(self):
        pass


#
#    def from_toml(f):
#        pass
#
#    def to_toml(f):
#        pass
#
#    
#    @property
#    @classmethod
#    def env(cls, name):
#        """Environment variable name"""
#
#        def normalize(name):
#            name = name.replace("-", "_")
#            name = name.upper()
#            return name
#
#        return normalize(name)
#
#    @property
#    @classmethod
#    def cli(cls):
#        """Cli argument name"""
#
#        def normalize(name):
#            name = name.replace("_", "-")
#            name = name.lower()
#            return name
#
#        return f"--{normalize(name)}"
#
#
