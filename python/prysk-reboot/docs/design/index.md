# Design Doc

## Architecture

![architecture](../drawings/architecture.drawio)

## Formats
This section describes various formats supported and used by the prysk engine.


### Prysk Input Format
The [prysk-input-format](../resources/schemas/prysk-input-fromat.schema) format is used by the prysk engine
as input format to define a single "unit" of work and it's context.
Bellow you can see and example file.

#### Example Input File
```json
{
  "name": "step/execution name",
  "environment": {
    "working-dir": "if empty executor will provide one",
    "env": ""
  },
  "runtime": {
    "type": "generic-runtime",
    "parameters": {
      "command": "python",
      "arguments": [
        "-m"
      ]
    }
  },
  "target": {
    "type": "generic-target",
    "command": "json.tool",
    "arguments": [
      "--indent",
      "content.json"
    ]
  },
  "inputs": [
    {
      "type": "stdin",
      "name": "stdin",
      "parameters": {
        "format": {
          "type": "text",
          "parameters": {
            "encoding": "utf-8"
          }
        }
      }
    }
  ],
  "outputs": [
    {
      "type": "exit-code",
      "name": "exit-code",
      "format": {
        "type": "text",
        "parameters": {
          "encoding": "utf-8"
        }
      }
    },
    {
      "type": "stdout",
      "name": "stdout",
      "format": {
        "type": "text",
        "parameters": {
          "encoding": "utf-8"
        }
      }
    },
    {
      "type": "stderr",
      "name": "stderr",
      "format": {
        "type": "text",
        "parameters": {
          "encoding": "utf-8"
        }
      }
    }
  ],
  "expectations": [
    {
      "comparator": {
        "type": "text-diff"
      },
      "old": {
        "type": "exit-code",
        "expected-exit-code": 0
      },
      "new": "exit-code"
    },
    {
      "comparator": {
        "type": "text-diff"
      },
      "old": {
        "type": "file",
        "path": "/AProject/Specification/RequirementXYZ.md",
        "format": {
          "type": "text",
          "encoding": "utf-8"
        },
        "location": {
          "offset": 100,
          "length": 100
        }
      },
      "new": "stdout"
    },
    {
      "comparator": {
        "type": "no-diff"
      },
      "old": {},
      "new": "stderr"
    }
  ]
}
```
