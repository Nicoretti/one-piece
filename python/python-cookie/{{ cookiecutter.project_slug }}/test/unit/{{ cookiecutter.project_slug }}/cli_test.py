import pytest
from {{ cookiecutter.project_slug }}.cli import SUCCESS, FAILURE


def test_cli_constant_success():
    assert SUCCESS == 0

def test_cli_constant_failure():
    assert FAILURE == -1
