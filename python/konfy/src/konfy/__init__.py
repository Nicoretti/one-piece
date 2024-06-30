from __future__ import annotations

from collections import abc
import os
from collections import defaultdict, ChainMap
from typing import (
    Any,
    Callable,
    MutableMapping,
)


class Konfy:
    def __init__(
        self,
        application: str,
        cli=None,
        environment=None,
        app_config=None,
        user_config=None,
        system_config=None,
        defaults=None,
    ):
        """
        Initializes a Konfy object to manage configuration settings.

        Args:
            application: str. Name of the application the Konfy object is for.
            cli: dict or argparse.Namespace, optional. Parsed command line arguments.
                Default is None.
            environment: dict, optional. Environment variables. Default is None,
                which uses os.environ.
            app_config: str, optional. Path to the application configuration file.
                Default is <current working directory>/<application>.toml.
            user_config: str, optional. Path to the user-specific configuration file.
                Default is OS-specific (e.g., Linux: ~/config/<application>/config.toml).
            system_config: str, optional. Path to the system-wide configuration file.
                Default is OS-specific (e.g., Linux: /etc/<application>.toml).
            defaults: dict, optional. A dictionary containing the default settings
                for the application. Default is None.
        """
        self._app = application
        self._cli = cli or {}
        self._environment = environment or {}
        self._app_config = app_config or {}
        self._user_config = user_config or {}
        self._system_config = system_config or {}
        self._defaults = defaults or {}

    @property
    def config(self) -> Config:
        return Config(
            self._cli,
            self._environment,
            self._app_config,
            self._user_config,
            self._system_config,
            self._defaults,
        )


class Attributes:
    def __init__(self, dictionary=None, /, **kwargs):
        self._dict = dictionary or {}
        self._dict.update(kwargs)

    def __getattr__(self, name):
        try:
            value = self._dict[name]
        except KeyError as ex:
            raise AttributeError(f"'Attributes' object has no attribute '{name}'") from ex

        value = Attributes(value) if issubclass(type(value), abc.Mapping) else value
        return value

    def __getitem__(self, key):
        value = self._dict[key]
        value = Attributes(value) if issubclass(type(value), abc.Mapping) else value
        return value

    def __iter__(self):
        return iter(self._dict)

    def __len__(self):
        return len(self._dict)

    def __repr__(self):
        return f"Config({self._dict})"

    def __str__(self):
        return str(self._dict)


class Config(abc.Mapping):

    def __init__(self, *dicts):
        self._config = ChainMap(*dicts)
        self._dict = Attributes(self._config)

    def __getattr__(self, name):
        return self._dict[name]

    def __getitem__(self, key):
        return self._config[key]

    def __iter__(self):
        return iter(self._dict)

    def __len__(self):
        return len(self._dict)

    def __repr__(self):
        return f"Config({self._dict})"

    def __str__(self):
        return str(self._dict)


def from_string(value: str, data_type: Any) -> Any:
    """Transform a type from env var string to a specific data type."""
    if hasattr(data_type, "from_string"):
        return data_type.from_string(value)
    converters = {bool: to_bool, int: to_int, str: to_string, float: to_float}
    converter: Callable[[str], Any] = converters[data_type]
    return converter(value)


def to_bool(value: str) -> bool:
    """Convert string to a boolean value."""
    value = value.lower()
    mapping = defaultdict(
        bool,
        {
            "": False,
            None: False,
            "true": True,
            "false": False,
            "no": False,
            "yes": True,
            "on": True,
            "off": False,
        },
    )
    if value.isdigit():
        return int(value, base=0) != 0
    return mapping[value]


def to_int(value: str) -> int:
    """Convert string to a integer value."""
    return int(value, base=0)


def to_float(value: str) -> float:
    """Convert string to float."""
    return float(value)


def to_string(value: Any) -> str:
    """Convert a value to it's env var compatible string representation."""
    if isinstance(value, str):
        return value
    if hasattr(value, "to_string"):
        converter: Callable[[], str] = value.to_string
        return converter()
    if isinstance(value, bool):
        return "ON" if value else "OFF"
    return f"{value}"


def env_key(name: str, prefix: str) -> str:
    """Based on the settings name and the prefix return a valid/normalized env key."""

    # pylint: disable=C0116
    def normalize(n: str) -> str:
        mappings = {"-": "_", ".": "_"}
        for character, replacement in mappings.items():
            n = n.replace(character, replacement)
        return n.upper()

    prefix = f"{prefix}_" if prefix else ""
    key = prefix + name
    return normalize(key)


def from_env(
    name: str,
    data_type: Any,
    prefix: str = "",
    env: MutableMapping[str, str] | None = None,
) -> Any:
    """Read a specific environment variable from env."""
    env = env if env else os.environ
    key = env_key(name, prefix)
    value = env[key]
    return from_string(value, data_type)


def to_env(
    name: str, obj: Any, prefix: str = "", env: MutableMapping[str, str] | None = None
) -> MutableMapping[str, str]:
    """Write a specific value back to the environment."""
    env = env if env is not None else os.environ
    key = env_key(name, prefix)
    obj = to_string(obj)
    env[key] = obj
    return env
