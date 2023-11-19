from __future__ import annotations

from datetime import datetime
from pathlib import Path

from pytest_history import report

DEFAULT_DB = ".test-results.db"


def pytest_configure(config):
    cwd: Path = Path(config.rootdir)
    db = cwd / DEFAULT_DB

    if not db.exists():
        report.SqlLite.create_db(db.name)

    test_reporter = report.SqlLite(db, f"{datetime.now()}")
    config.stash["sql-reporter"] = test_reporter
    config.pluginmanager.register(test_reporter)

    # TODO: Add support for pytest cli flag in order to support custom db file(s)
