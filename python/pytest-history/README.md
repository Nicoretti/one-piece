<h1 align="center">pytest-history</h1>
<p align="center">
Pytest plugin to keep history of your pytest runs
</p>

<p align="center">

<a href="https://github.com/Nicoretti/one-piece/python/pytest-history">
    <img src="https://img.shields.io/github/checks-status/nicoretti/crc/master" alt="Checks Master">
</a>
<a href="https://opensource.org/licenses/MIT">
    <img src="https://img.shields.io/pypi/l/pytest-history" alt="License">
</a>
<a href="https://pypi.org/project/pytest-history/">
    <img src="https://img.shields.io/pypi/pyversions/pytest-history" alt="Supported Python Versions">
</a>
<a href="https://pypi.org/project/pytest-history/">
    <img src="https://img.shields.io/pypi/v/pytest-history" alt="PyPi Package">
</a>
</p>

## Overview

`pytest-history` enables the tracking of test statuses and other metadata across multiple test runs, providing additional insights into test behavior.

Initially, this plugin was developed specifically to identify potentially flaky tests (approximately 200) within a test suite containing over 1000 tests, where various tests exhibited inconsistent behavior by failing on alternate runs.

## Purpose

- **Tracking Test History:** Capturing and storing historical test results, encompassing pass, fail, and other pertinent metadata.
- **Identifying Flaky Tests:** Enabling the identification of flaky tests by scrutinizing historical data, detecting irregularities or recurring patterns in test outcomes.
- **Facilitating Debugging:** Offering developers and testers insights into test stability, thereby assisting in debugging efforts and enhancing overall test reliability.

## Usage

1. Install the plugin using `pip install pytest-history`.
2. Utilize the historical data stored in `.test-results.db` (SQLite database).

## Example Queries

Example: To find flaky tests between two distinct test runs, execute the following SQL query:

```sql
SELECT t1.testcase, t1.test_run, t2.test_run, t1.outcome, t2.outcome
FROM "test.results" t1
JOIN "test.results" t2 on t1.testcase = t2.testcase AND (t1.test_run = 1 AND t2.test_run = 2)
WHERE (t1.outcome = 'passed' AND t2.outcome = 'failed')
   OR (t1.outcome = 'failed' AND t2.outcome = 'passed')
GROUP BY t1.testcase
ORDER BY t1.testcase;
```
