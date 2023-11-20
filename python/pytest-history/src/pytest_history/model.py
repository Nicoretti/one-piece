from __future__ import annotations

import datetime
from dataclasses import dataclass


@dataclass(frozen=True)
class TestResult:
    id: int
    test_run: int
    node_id: str
    file: str
    lineno: int
    testcase: str
    outcome: str
    skipped: str
    duration: float


@dataclass(frozen=True)
class TestRun:
    id: int
    start: datetime.datetime
