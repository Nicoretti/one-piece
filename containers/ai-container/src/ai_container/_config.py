"""Layered configuration for ai-container.

Settings are merged from several sources, highest precedence first:

1. Command-line flags (applied in :mod:`ai_container.cli`).
2. ``./.ai-container.toml`` in the current working directory (per project).
3. ``$XDG_CONFIG_HOME/ai-container/config.toml`` (defaults to
   ``~/.config/ai-container/config.toml``).
4. ``~/.ai-container.toml`` in the user's home directory.
5. Built-in defaults.

All file names share the ``ai-container`` prefix and a ``.toml`` suffix so the
format and ownership are obvious at a glance. The original idea mixed
``.ai-container`` (cwd) with ``.ai-config`` (home); unifying the names keeps the
mental model simple -- the same settings live under the same name everywhere.
"""

from __future__ import annotations

import logging
import tomllib
from collections import ChainMap
from pathlib import Path

from ai_container._podman import BASE_ENV, config_dir

log = logging.getLogger(__name__)

#: File name used for the project-local and home dotfiles.
DOTFILE = ".ai-container.toml"
#: File name used inside the XDG config directory.
CONFIG_NAME = "config.toml"

#: Recognised settings and their built-in defaults (also fixes their types).
DEFAULTS = {
    "env": BASE_ENV,
    "log_level": "INFO",
    "dryrun": False,
}


class ConfigError(Exception):
    """Raised when a config file is malformed or contains invalid settings."""


def config_paths() -> list[Path]:
    """Return the config file locations, highest precedence first."""
    return [
        Path.cwd() / DOTFILE,
        config_dir() / CONFIG_NAME,
        Path.home() / DOTFILE,
    ]


def _validate(path: Path, data: dict) -> dict:
    """Reject unknown settings and type mismatches in one config file."""
    for key, value in data.items():
        if key not in DEFAULTS:
            valid = ", ".join(DEFAULTS)
            raise ConfigError(f"{path}: unknown setting '{key}' (valid: {valid}).")
        expected = type(DEFAULTS[key])
        if not isinstance(value, expected):
            raise ConfigError(f"{path}: '{key}' must be of type {expected.__name__}.")
    return data


def _load(path: Path) -> dict:
    """Parse and validate one TOML config file (empty dict if absent)."""
    if not path.is_file():
        log.info("No config at %s", path)
        return {}
    try:
        with path.open("rb") as handle:
            data = tomllib.load(handle)
    except (OSError, tomllib.TOMLDecodeError) as exc:
        raise ConfigError(f"{path}: could not read config ({exc}).") from exc
    data = _validate(path, data)
    log.info("Loaded config from %s: %s", path, data)
    return data


def load_config() -> ChainMap:
    """Return the merged configuration, file layers stacked over the defaults.

    The result is a :class:`~collections.ChainMap`; earlier maps (higher
    precedence) win, and :data:`DEFAULTS` at the bottom guarantees every known
    key resolves to a value.
    """
    layers = [_load(path) for path in config_paths()]
    merged = ChainMap(*layers, DEFAULTS)
    log.info("Resolved config: %s", dict(merged))
    return merged
