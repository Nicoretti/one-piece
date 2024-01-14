from __future__ import annotations

import sqlite3
from inspect import cleandoc

from pytest_history.model import TestResult, TestRun


def flakes(db):
    query = cleandoc(
        """
        SELECT 
            NULL as id,
            NULL as test_run,
            t1.node_id,
            t1.file,
            t1.lineno,
            t1.testcase,
            NULL as outcome,
            NULL as skipped,
            t1.duration 
        FROM "test.results" t1
        JOIN "test.results" t2 on t1.testcase = t2.testcase AND (t1.test_run <>  t2.test_run)
        WHERE (t1.outcome = 'passed' AND t2.outcome = 'failed')
           OR (t1.outcome = 'failed' AND t2.outcome = 'passed')
        GROUP BY t1.testcase
        ORDER BY t1.testcase;
        """
    )
    with sqlite3.connect(db) as con:
        flakes = con.execute(query)
        yield from (TestResult(*flake) for flake in flakes)


def runs(db):
    query = 'SELECT id, start FROM "test.runs";'
    with sqlite3.connect(db) as con:
        runs = con.execute(query)
        yield from (TestRun(*run) for run in runs)


def results(db, id):
    query = cleandoc(
        """
        SELECT 
            id,
            test_run,
            node_id,
            file,
            lineno,
            testcase,
            outcome,
            skipped,
            duration 
        FROM "test.results"
        WHERE test_run = ?
        ORDER BY testcase;
        """
    )
    with sqlite3.connect(db) as con:
        results = con.execute(query, (id,))
        yield from (TestResult(*result) for result in results)


def newly_added(db):
    query = cleandoc(
        """
        SELECT id,
        test_run,
        node_id,
        file,
        lineno,
        testcase,
        outcome,
        skipped,
        duration
        FROM "test.results"
        WHERE node_id NOT IN (
            SELECT node_id
            FROM "test.results"
            WHERE test_run != (SELECT MAX(id) FROM "test.runs"))
        ORDER BY testcase;
        """
    )
    with sqlite3.connect(db) as con:
        results = con.execute(query)
        yield from (TestResult(*result) for result in results)


def added_since(db, since):
    query = cleandoc(
        """
        SELECT id,
        test_run,
        node_id,
        file,
        lineno,
        testcase,
        outcome,
        skipped,
        duration
        FROM "test.results"
        WHERE node_id NOT IN (
            SELECT node_id
            FROM "test.results"
            WHERE test_run < ? )
        ORDER BY testcase;
        """
    )
    with sqlite3.connect(db) as con:
        results = con.execute(query, since)
        yield from (TestResult(*result) for result in results)
