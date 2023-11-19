from __future__ import annotations

import sqlite3
from inspect import cleandoc

from pytest import Pytester
from pytest_history import DEFAULT_DB

pytest_plugins = "pytester"


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
    test = cleandoc(
        f"""
        from pathlib import Path

        def test_pass():
            db = Path("{DEFAULT_DB}")
            assert db.exists()
        """
    )
    pytester.makepyfile(passing_test=test)
    pytester.runpytest()

    with sqlite3.connect(DEFAULT_DB) as con:
        query = "SELECT name FROM sqlite_master WHERE type=? AND name=?;"
        result = con.execute(query, ("table", "test.results")).fetchall()
        expected = 1
        actual = len(result)
        assert actual == expected


def test_plugin_creates_history_table_for_test_runs(pytester: Pytester):
    test = cleandoc(
        f"""
        from pathlib import Path

        def test_pass():
            db = Path("{DEFAULT_DB}")
            assert db.exists()
        """
    )
    pytester.makepyfile(passing_test=test)
    pytester.runpytest()

    with sqlite3.connect(DEFAULT_DB) as con:
        query = "SELECT name FROM sqlite_master WHERE type=? AND name=?;"
        result = con.execute(query, ("table", "test.runs")).fetchall()
        expected = 1
        actual = len(result)
        assert actual == expected
