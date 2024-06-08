from typing import Generic, TypeVar
from dataclasses import dataclass
from aergia._config import _env

T = TypeVar("T")


@dataclass(frozen=True)
class Setting(Generic[T]):
    name: str
    value: T | None = None
    prefix: str | None = None
    type: T = T
    default: T | None = None
    description: str = ""

    def __to_envkey__(self):
        name = f"{self.prefix}-" if self.prefix is not None else ""
        name += self.name
        name = _env.normalize(name)
        return f"{name}"

    def __to_str__(self):
        value = self.value if self.value is not None else self.default
        if value is None:
            return ""
        return f"{value}"

    def __from_str__(self, string):
        return self.type(string)


class Namespace:
    name: str
    settings: list
    description: str = ""
