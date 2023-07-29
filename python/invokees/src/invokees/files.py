"""Automation tasks for the crc project"""
from collections.abc import Iterable
from pathlib import Path


def python_files(
    project_root: Path, path_filters: Iterable[str] = ("dist", ".eggs", "venv")
) -> Iterable[Path]:
    """Returns all relevant"""
    return deny_filter(project_root.glob("**/*.py"), deny_list=path_filters)


def deny_filter(files: Iterable[Path], deny_list: Iterable[str]) -> Iterable[Path]:
    """
    Adds a filter to remove unwanted paths containing python files from the iterator.
     args:
     return:
    """
    for entry in deny_list:
        files = filter(lambda path: entry not in path.parts, files)
    return files
