from invoke import task

from invokees.tasks import command


def _coverage():
    return ["coverage", "run", "-m", "-a"]


def _pytest(path):
    return ["pytest", path]


@task
def test(context, testdir="./test", cov=False, color=True):
    """
    Run all tests

    Args:
        context: invoke context.
        testdir: containing the test files (default: './test').
        cov: whether to record code coverage (default: False).
        color: whether to use colors (default: True).
    """
    cmd = _coverage() if cov else []
    cmd += _pytest(testdir)
    context.run(command(*cmd), pty=color)


@task(aliases=("ut",))
def unit(context, testdir="./test/unit", cov=False, color=True):
    """
    Run all unit tests

    Args:
        context: invoke context.
        testdir: containing the test files (default: './test/unit').
        cov: whether to record code coverage (default: False).
        color: whether to use colors (default: True).
    """
    cmd = _coverage() if cov else []
    cmd += _pytest(testdir)
    context.run(command(*cmd), pty=color)


@task(aliases=("it",))
def integration(context, testdir="./test/integration", cov=False, color=True):
    """
    Run all unit tests

    Args:
        context: invoke context.
        testdir: containing the test files (default: './test/integration').
        cov: whether to record code coverage (default: False).
        color: whether to use colors (default: True).
    """
    cmd = _coverage() if cov else []
    cmd += _pytest(testdir)
    context.run(command(*cmd), pty=color)


@task(aliases=("cov",))
def coverage(context, testdir="./test", color=True):
    """
    Run all tests and report test coverage

    Args:
        context: invoke context.
        testdir: containing the test files (default: './test').
        color: whether to use colors (default: True).
    """
    cmd = _coverage() + _pytest(testdir)
    context.run(command(*cmd), pty=color)
    context.run(command("coverage", "report"), pty=color)
