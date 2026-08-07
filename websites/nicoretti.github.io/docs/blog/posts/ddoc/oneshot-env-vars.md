---
date: 2024-04-26
categories:
  - DDOC
  - CLI
  - ENV
  - TERMINAL
  - SHELL
---

# Daily Dose Of CLI \#2

## Oneshot ENVIRONMENT Variable(s)

In various shells, it is possible to create a temporary environment variable for a specific process and its children by defining them immediately before the shell command that spawns the process.

Command:
```shell
TMP1="Hello," TMP2="World" bash -c 'echo $TMP1 $TMP2!'
```
Output:
```
Hello, World!
```

Command:
```shell
TMP="Temp ENV VAR" env
```
Output:
```
...
TMP=Temp ENV VAR
...
```

### References
* [Bash Refernce](https://www.gnu.org/software/bash/manual/bash.html#Environment)
