from __future__ import annotations
import pytest

import sqlite3
from inspect import cleandoc

from pytest import Pytester

from pytest_history import DEFAULT_DB

pytest_plugins = "pytester"


@pytest.mark.xfail
def test_xfail(pytester: Pytester):
    assert False


@pytest.mark.skip
def test_skip(pytester: Pytester):
    assert False


def test_fail(pytester: Pytester):
    assert False


def test_plugin_creates_default_database(pytester: Pytester):
    test = cleandoc(
        f"""
        from pathlib import Path
         
        def test_pass():
            db = Path("{DEFAULT_DB}")
            assert db.exists()
        """
    )
    pytester.makepyfile(passing_test=test)
    result = pytester.runpytest()

    expected = 0
    actual = result.ret

    assert actual == expected


def test_plugin_creates_history_table_for_test_results(pytester: Pytester):
    pass


def test_plugin_creates_history_table_for_test_results(pytester: Pytester):
    pass


def test_plugin_creates_history_table_for_test_runs(pytester: Pytester):
    test = cleandoc(
        """
        def test_pass():
            assert True
        """
    )
    pytester.makepyfile(passing_test=test)
    results = pytester.runpytest()

    with sqlite3.connect("metrics.db") as con:
        table_name = "test_results"
        query = "SELECT name FROM [sqlite_master] WHERE type='table' and name=?;"
        result = con.execute(query, (table_name,))
        result = result.fetchall()

    expected = 1
    actual = len(result)

    assert actual == expected
