"""Automation tasks for the website project"""
import shutil
from pathlib import Path
from typing import Iterable
from tempfile import TemporaryDirectory
from rich.console import Console
from rich.table import Table
from invoke import (
    Collection,
    task,
)
from invoke.main import program

BASEPATH = Path(__file__).parent.resolve()

_console = Console()

_REQUIRED_COMMANDS = ['aspell', 'git']


class MissingSystemCommandError(Exception):
    """Required system command is missing"""


def _markdown_files(
        path: Path, path_filters: Iterable[str] = ("scratch",)
) -> Iterable[Path]:
    """Returns all relevant"""
    return _deny_filter(path.glob("**/*.md"), deny_list=path_filters)


def _deny_filter(files: Iterable[Path], deny_list: Iterable[str]) -> Iterable[Path]:
    """
    Adds a filter to remove unwanted paths containing python files from the iterator.
     args:
     return:
    """
    for entry in deny_list:
        files = filter(lambda path: entry not in path.parts, files)
    return files


@task(aliases=['spell'])
def spellcheck(ctx):
    """
    Runs a spellchecker on the workspace.
    """
    _are_all_required_commands_available()
    files = _markdown_files(BASEPATH / 'docs')

    def _errors_in_file(f):
        cmd = "aspell --lang=en --mode=markdown list < {file}"
        command = cmd.format(file=file)
        result = ctx.run(command, hide=True)
        findings = result.stdout.split('\n')
        yield from (f for f in findings if f)

    table = Table()
    table.add_column("Spelling", style="red", no_wrap=True)
    table.add_column("Location", style="cyan")

    for file in files:
        for error in _errors_in_file(file):
            table.add_row(error, f"{file}")

    _console.print(table)


@task
def publish(ctx, version=None):
    """Builds and publishes the current state of the workspace."""
    repo_name = 'nicoretti.github.io'
    repo_url = f"git@github.com:Nicoretti/{repo_name}.git"

    if not version:
        version = ctx.run('git rev-parse --short HEAD', hide=True).stdout.strip()

    with TemporaryDirectory() as tmp_dir:
        tmp_dir = Path(tmp_dir)
        checkout_path = tmp_dir / repo_name
        git_dir = f"--git-dir={checkout_path / '.git'}"
        work_tree = f"--work-tree={checkout_path}/"

        ctx.run(f"git clone {repo_url} {checkout_path}")
        ctx.run(f"git {git_dir} branch -m master old-master")
        ctx.run(f"git {git_dir} checkout --orphan master")
        ctx.run(f"mkdocs build -c -s -d {checkout_path}/ -f {BASEPATH / 'mkdocs.yml'}")
        ctx.run(f"git {git_dir} {work_tree} add {checkout_path}/")
        ctx.run(f'git {git_dir} commit -m "Publish version: {version}"')
        ctx.run(f"git {git_dir} push -f origin master")


def _are_all_required_commands_available():
    for command in _REQUIRED_COMMANDS:
        if not shutil.which(command):
            raise MissingSystemCommandError(command)


namespace = Collection()
namespace.add_task(spellcheck, name="spell-check")
namespace.add_task(publish, name="publish")

if __name__ == "__main__":
    _are_all_required_commands_available()
    program.run()
