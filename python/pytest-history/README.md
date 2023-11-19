
Example: Find flaky tests between two different test runs.

```sql
SELECT t1.testcase, t1.test_run, t2.test_run, t1.outcome, t2.outcome
FROM "test.results" t1
JOIN "test.results" t2 on t1.testcase = t2.testcase AND (t1.test_run = 1 AND t2.test_run = 2)
WHERE (t1.outcome = 'passed' AND t2.outcome = 'failed')
   OR (t1.outcome = 'failed' AND t2.outcome = 'passed')
GROUP BY t1.testcase
ORDER BY t1.testcase;
```