from __future__ import annotations
from typing import Generic, TypeVar
from collections import ChainMap
from dataclasses import dataclass

DB_NAME = 'aergia'

T = TypeVar("T")


@dataclass(frozen=True)
class setting(Generic[T]):
    name: str
    prefix: str
    type: T
    default: T | None
    help_text: str = ""

    @property
    def env(self):
        """Environment variable name"""

        def normalize(name):
            name = name.replace("-", "_")
            name = name.upper()
            return name

        return f"{normalize(self.prefix)}_{normalize(self.name)}"

    @property
    def cli(self):
        """Cli argument name"""

        def normalize(name):
            name = name.replace("_", "-")
            name = name.lower()
            return name

        return f"--{normalize(self.prefix)}-{normalize(self.name)}"

    @property
    def pytest(self):
        """Pytest option name"""

        def normalize(name):
            name = name.replace("-", "_")
            name = name.lower()
            return name

        return f"{normalize(self.prefix)}_{normalize(self.name)}"

    @property
    def help(self):
        """Help text including information about default value."""
        if not self.default:
            return f"{self.help_text}."
        return f"{self.help_text} (default: {self.default})."


def load_settings(cli, environment, config, defaults):
    settings = ChainMap(cli, environment, config, defaults)
    return settings
