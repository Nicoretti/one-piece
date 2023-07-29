from pathlib import Path

from invoke import task

from invokees.files import python_files
from invokees.tasks import command


@task(name="format", aliases=("fmt",))
def format(context, root=".", fix=True, color=True):  # noqa: A001
    """
    Apply code formatter(s)

    Args:
        context: invoke context.
        root: to search for python files (default: '.').
        fix: issues instead of reporting them (default: True).
        color: whether to use colors (default: True).
    """
    root = Path(root)
    files = list(python_files(root))
    fixable_rules = {
        "isort": "I",
        "flake 8 tidy imports": "TID",
        "flake 8 import conventions": "ICN",
        "unused import": "F401",
    }
    ruff = [
        "ruff",
        "check",
        "--fix" if fix else "",
        "--exit-zero" if fix else "",
        f"--select {','.join(fixable_rules.values())}",
    ] + files
    context.run(command(*ruff), pty=color)

    isort = ["isort", "--check" if not fix else ""] + files
    context.run(command(*isort), pty=color)

    black = ["black", "--check" if not fix else "", "--color" if color else ""] + files
    context.run(command(*black), pty=color)


@task
def lint(context, root=".", fix=True, color=True):
    """
    Run linter on project

    Args:
        context: invoke context.
        root: to search for python files (default: '.').
        fix: fixable issues instead of reporting them (default: True).
        color: whether to use colors (default: True).
    """
    root = Path(root)
    files = list(python_files(root))
    ruff = ["ruff", "check", "--fix" if fix else "", "--exit-non-zero-on-fix"] + files
    context.run(command(*ruff), pty=color)


@task
def sentry(context, root=".", color=True):
    """
    Run linter in sentry/watch mode

    Args:
        context: invoke context.
        root: to search for python files (default: '.').
        color: whether to use colors (default: True).
    """
    root = Path(root)
    files = list(python_files(root))
    ruff = ["ruff", "check", "--watch"] + files
    context.run(command(*ruff), pty=color)


@task
def typing(context, root=".", color=True):
    """
    Run linter in sentry/watch mode

    Args:
        context: invoke context.
        root: to search for python files (default: '.').
        color: whether to use colors (default: True).
    """
    root = Path(root)
    files = list(python_files(root))
    mypy = ["mypy"] + files
    context.run(command(*mypy), pty=color)
