from __future__ import annotations

from collections import ChainMap, abc


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
    def config(self) -> Resolver:
        return Resolver(
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
            raise AttributeError(
                f"'Attributes' object has no attribute '{name}'"
            ) from ex

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
        return f"{type(self).__name___}({self._dict})"

    def __str__(self):
        return str(self._dict)


class Resolver(abc.Mapping):
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
        return f"{type(self).__name___}({self._dict})"

    def __str__(self):
        return str(self._dict)
