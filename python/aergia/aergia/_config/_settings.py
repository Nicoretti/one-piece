from pathlib import Path
from collections import ChainMap
from aergia._config._toml import from_toml

DEFAULT_CONFIG = Path.home() / ".aergia.toml"


def settings_from(args, config):
    args = vars(args)
    cfg = from_toml(config)
    settings = ChainMap(args, cfg)
    return settings
