import pytest
import json
from dataclasses import dataclass, field
from typing import List, Dict
from aergia._roles import parse, load, render, execute, RoleNotFound


@dataclass(frozen=True)
class Expected:
    role: str
    args: List[str] = field(default_factory=list)
    kwargs: Dict[str, str] = field(default_factory=dict)


def id_func(param):
    if isinstance(param, Expected):
        return f"{param}"
    return param


@pytest.mark.parametrize("role_spec,expected", [
    ("role", Expected(role="role", args=[], kwargs={})),
    ("role:arg1", Expected(role="role", args=["arg1"], kwargs={})),
    ("role:arg1:arg2:arg3", Expected(role="role", args=["arg1", "arg2", "arg3"], kwargs={})),
    ("role:kwarg1=1", Expected(role="role", args=[], kwargs={"kwarg1": "1"})),
    (
            "role:kwarg1=1:kwarg2=2:kwarg3=3",
            Expected(role="role", args=[], kwargs={"kwarg1": "1", "kwarg2": "2", "kwarg3": "3"})
    ),
    (
            "role:arg1:kwarg1=1:kwarg2=2:arg2",
            Expected(role="role", args=["arg1", "arg2"], kwargs={"kwarg1": "1", "kwarg2": "2"})
    ),
    (
            "role:kwarg1=1:arg1:kwarg2=2:arg2",
            Expected(role="role", args=["arg1", "arg2"], kwargs={"kwarg1": "1", "kwarg2": "2"})
    ),
], ids=id_func)
def test_parse_role(role_spec, expected):
    role, args, kwargs = parse(role_spec)
    assert role == expected.role
    assert args == expected.args
    assert kwargs == expected.kwargs


def test_load_builtin_role_template():
    expected = ("typos.role", {'arguments': {'amount': 0}})
    template, metadata = load("typos")
    actual = (template.name, metadata)
    assert actual == expected


@pytest.fixture
def test_role():
    name = "test"
    content = "This is just a test role"
    metadata = {}
    yield name, content, metadata


@pytest.fixture
def test_role_on_fs(tmp_path, test_role):
    name, content, metadata = test_role
    role_definition = tmp_path / f"{name}.role"
    role_definition.write_text(content)
    role_metadata = tmp_path / f"{name}.role.meta"
    role_metadata.write_text(json.dumps(metadata))
    yield name, tmp_path


def test_load_custom_role_template(test_role_on_fs):
    name, path = test_role_on_fs
    template, metadata = load(name, paths=[path])
    expected = ("test.role", {})
    actual = (template.name, metadata)
    assert actual == expected


def test_failed_to_load_role():
    with pytest.raises(RoleNotFound):
        template, metadata = load("this-role-should-not-exist")


def test_render():
    expected = (
        "Keep the structure and formatting as is, "
        "only fix all typos and spelling errors in the text below:\n"
        "Helo, how are you?"
    )
    template, _ = load("typos")
    actual = render(template, [], kwargs={}, input="Helo, how are you?")
    assert actual == expected


def test_execute_kw_arg():
    expected = (
        "Please translate the text below to german:\n"
        "Hello how are you?"
    )
    role_spec = "babelfish:lang=german"
    input = "Hello how are you?"
    actual = execute(role_spec, input=input)
    assert actual == expected


def test_execute_arg():
    expected = (
        "Please translate the text below to german:\n"
        "Hello how are you?"
    )
    role_spec = "babelfish:german"
    input = "Hello how are you?"
    actual = execute(role_spec, input=input)
    assert actual == expected
