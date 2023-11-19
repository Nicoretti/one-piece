from __future__ import annotations

import sqlite3
from inspect import cleandoc
from pathlib import Path


class SqlLite:
    def __init__(self, db, test_run):
        def ensure_test_runs_table_exists(name):
            with sqlite3.connect(name) as con:
                query = cleandoc(
                    """
                    CREATE TABLE IF NOT EXISTS [test.runs] (
                        id integer primary key,
                        start text
                    );
                    """
                )
                con.execute(query)

        def ensure_test_results_table_exists(name):
            with sqlite3.connect(name) as con:
                query = cleandoc(
                    """
                    CREATE TABLE IF NOT EXISTS [test.results] (
                        id integer primary key,
                        test_run integer not null,
                        node_id text,
                        file text,
                        lineno integer,
                        testcase text,
                        outcome text,
                        skipped text,
                        duration real,
                        foreign key (test_run) REFERENCES [test.runs](id)
                    );
                    """
                )
                con.execute(query)

        def add_test_run_entry(name, run):
            with sqlite3.connect(name) as con:
                query = "INSERT INTO [test.runs] (start) VALUES (?);"
                result = con.execute(query, (run,))
                return result.lastrowid

        self._db = db
        ensure_test_runs_table_exists(db)
        ensure_test_results_table_exists(db)
        self._test_run = add_test_run_entry(db, test_run)

    def pytest_runtest_logreport(self, report):
        if report.when != "teardown":
            return
        self.report(report)

    def report(self, test):
        with sqlite3.connect(self._db) as con:
            query = cleandoc(
                """
                INSERT INTO [test.results] (
                    test_run,
                    node_id,
                    file,
                    lineno,
                    testcase,
                    outcome,
                    duration
                )
                VALUES (?, ?, ?, ?, ?, ?, ? );
                """
            )
            file, lineno, testcase = test.location
            con.execute(
                query,
                (
                    self._test_run,
                    test.nodeid,
                    file,
                    lineno,
                    testcase,
                    test.outcome,
                    test.duration,
                ),
            )

    @staticmethod
    def create_db(name: str | Path) -> str | Path:
        with sqlite3.connect(name) as _:
            # we only want to create a empty db file
            pass
        return name
