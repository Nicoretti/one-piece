---
draft: true
date: 2022-01-01
categories:
  - CLI
  - Shell
  - ENV
  - Environment-Variables
---

# Environment Variables
In this blog article I want to focus on Environment variables, especially in the context
of command line tools.

In the tips & tricks section you main find some helpful tricks.

```shell
user@host ~ $ FOO="BAR" env | grep "FOO"
FOO=BAR
```

<!-- more -->

## Context
- local vs global

## Namespacing

## Tips & Tricks

* environment files
* types

```shell
user@host ~ $ FOO="BAR" env | grep "FOO"
FOO=BAR
```

```shell

user@host ~ $ FOO="BAR" BAR="FOO" env | grep "FOO"\|BAR"
FOO=BAR
BAR=FOO
```
