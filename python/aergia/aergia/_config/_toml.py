def toml_key(obj):
    return obj.__to_envkey__()


def from_toml(type, name, path):
    pass


def normalize(identifier):
    identifier = identifier.replace("-", "_")
    identifier = identifier.upper()
    return identifier
