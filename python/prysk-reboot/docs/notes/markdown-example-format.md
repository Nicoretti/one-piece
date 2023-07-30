# Test Description

## Open Questions
* How convey the information which code blocks input, command/script and output belong together

### test case

```json intput=stdin

```

```python test-scenario
import sys
import json

def test_function():
    print("some output")
    print(json.dumps({"some": "value"}), file=sys.stderr)
```

```text output=stdout encoding=utf8  
some output
```

```json output=stderr encoding=utf8  
{"some":  "value"}
```
