import tomli


def toml_key(obj):
    return obj.__to_envkey__()


def from_toml(path):
    with open(path, "rb") as f:
        data = tomli.load(f)
        return data


def normalize(identifier):
    identifier = identifier.replace("-", "_")
    identifier = identifier.upper()
    return identifier
