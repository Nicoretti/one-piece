import os


def env(obj):
    return (obj.__to_envkey__(), obj.__to_str__())


def env_key(obj):
    return obj.__to_envkey__()


def from_env(type, name, env=None):
    def boolean(v):
        true = ["yes", "true", "on", "enabled"]
        false = ["no", "false", "off", "disabled"]
        v = v.lower()
        if v in true:
            return True
        if v in false:
            return False

        raise ValueError(f"Connot convert value: {v}, to bool.")

    converts = {int: int, float: float, str: str, bool: boolean}
    if type not in converts:
        converter = getattr(type, "__from_str__", str)
    else:
        converter = converts[type]

    env = env or os.environ
    if name not in env:
        return None

    return converter(env[name])


def normalize(identifier):
    identifier = identifier.replace("-", "_")
    identifier = identifier.upper()
    return identifier
