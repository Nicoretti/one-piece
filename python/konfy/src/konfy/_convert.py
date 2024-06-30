from __future__ import annotations

import os
from collections import defaultdict
from typing import (
    Any,
    Callable,
    MutableMapping,
)


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
