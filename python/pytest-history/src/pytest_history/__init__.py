from __future__ import annotations

import os
from datetime import datetime
from pathlib import Path

import pytest

from pytest_history import report

DEFAULT_DB = ".test-results.db"


def pytest_addoption(parser: pytest.Parser):
    history = parser.getgroup("history")
    history.addoption(
        "--history-db", help=f"Sqlite db to write the data to [default: {DEFAULT_DB}]"
    )
    parser.addini(
        "history-db",
        f"Sqlite db to write the data to. [default: {DEFAULT_DB}]",
        type="string",
        default=DEFAULT_DB,
    )


def pytest_configure(config: pytest.Config):
    db_file = config.getini("history-db")
    db_file = os.environ.get("PYTEST_HISTORY_DB", db_file)
    db_file = config.option.history_db if config.option.history_db else db_file
    db_file = Path(db_file)

    if not db_file.exists():
        report.SqlLite.create_db(db_file.name)

    test_reporter = report.SqlLite(db_file, f"{datetime.now()}")
    config.stash["sql-reporter"] = test_reporter
    config.pluginmanager.register(test_reporter)
