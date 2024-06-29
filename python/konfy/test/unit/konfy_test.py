# Context: Where can a setting be stored/loaded from
# 0. default value
# 1. load global config
# 2. load local config
# 3. load from env
# 4. cli setting
from __future__ import annotations

from dataclasses import dataclass
from typing import (
    Any,
    MutableMapping,
    TypeVar,
)

import pytest

from konfy import (
    env_key,
    from_env,
    from_string,
    to_env,
    to_string,
)


@pytest.mark.parametrize(
    "expected,name,prefix",
    [
        ("SOME_VALUE", "some_value", ""),
        ("SOME_VALUE", "some_value", None),
        ("PREFIX_SOME_VALUE", "some_value", "PREFIX"),
        ("PREFIX_SOME_VALUE", "some_value", "prefix"),
        ("SOME_VALUE", "some-value", ""),
        ("PREFIX_SOME_VALUE", "some-value", "prefix"),
        ("SOME_VALUE", "some.value", ""),
        ("PREFIX_SOME_VALUE", "some.value", "prefix"),
    ],
)
def test_env_key(expected: str, name: str, prefix: str) -> None:
    assert expected == env_key(name, prefix)


@dataclass
class CustomType:
    def __init__(self, user: str, password: str):
        self._user = user
        self._password = password

    @classmethod
    def from_string(cls, value: str) -> CustomType:
        user, password = value.split(":")
        return cls(user, password)

    def to_string(self) -> str:
        return f"{self._user}:{self._password}"


@pytest.mark.parametrize(
    "expected,parameter,type",
    [
        (False, "0", bool),
        (True, "1", bool),
        (True, "True", bool),
        (True, "true", bool),
        (False, "False", bool),
        (False, "false", bool),
        (False, "No", bool),
        (True, "Yes", bool),
        (False, "no", bool),
        (True, "yes", bool),
        (0, "0", int),
        (1, "1", int),
        (1, "0x01", int),
        (17, "0x11", int),
        (1.2, "1.2", float),
        (0.0, "0.0", float),
        (0.0, "0", float),
        (9, "9", float),
        ("foo", "foo", str),
        (r"bar", r"bar", str),
        (CustomType("foo", "bar"), "foo:bar", CustomType),
        (CustomType("bar", "foo"), "bar:foo", CustomType),
    ],
)
def test_from_string(expected: Any, parameter: str, type: TypeVar) -> None:
    assert expected == from_string(parameter, type)


@pytest.mark.parametrize(
    "expected,obj",
    [
        ("1", 1),
        ("123", 123),
        ("1.0", 1.0),
        ("123.0", 123.0),
        ("ON", True),
        ("OFF", False),
        ("foo:bar", CustomType("foo", "bar")),
        ("bar:foo", CustomType("bar", "foo")),
    ],
)
def test_to_string(expected: str, obj: Any) -> None:
    assert expected == to_string(obj)


@pytest.mark.parametrize(
    "expected,name,type,prefix,env",
    [
        (1, "foo", int, None, {"FOO": "1"}),
        (1, "FOO", int, None, {"FOO": "1"}),
        (1, "foo", int, "PREFIX", {"PREFIX_FOO": "1"}),
        (True, "DEBUG", bool, "PREFIX", {"PREFIX_DEBUG": "ON"}),
        (False, "DEBUG", bool, "PREFIX", {"PREFIX_DEBUG": "OFF"}),
        (False, "DEBUG", bool, "PREFIX", {"PREFIX_DEBUG": "False"}),
        (True, "DEBUG", bool, "PREFIX", {"PREFIX_DEBUG": "True"}),
        (1.0, "FOO", float, None, {"FOO": "1.0"}),
        (
            CustomType("user", "password"),
            "creds",
            CustomType,
            None,
            {"CREDS": "user:password"},
        ),
        (
            CustomType("user", "password"),
            "creds",
            CustomType,
            "PREFIX",
            {"PREFIX_CREDS": "user:password"},
        ),
    ],
)
def test_from_env(
    expected: Any, name: str, type: TypeVar, prefix: str, env: MutableMapping[str, str]
) -> None:
    assert expected == from_env(name, type, prefix, env)


@pytest.mark.parametrize(
    "expected,name,obj,prefix,env",
    [
        ({"FOO": "1"}, "foo", 1, None, {}),
        ({"PREFIX_FOO": "1"}, "foo", 1, "PREFIX", {}),
        ({"DEBUG": "ON"}, "DEBUG", True, None, {}),
        ({"DEBUG": "OFF"}, "DEBUG", False, None, {}),
        ({"FLOAT": "1.0"}, "float", 1.0, None, {}),
        (
            {"CREDS": "user:password"},
            "creds",
            CustomType("user", "password"),
            None,
            {},
        ),
    ],
)
def test_to_env(
    expected: MutableMapping[str, str],
    name: str,
    obj: Any,
    prefix: str,
    env: MutableMapping[str, str],
) -> None:
    assert expected == to_env(name, obj, prefix, env)
