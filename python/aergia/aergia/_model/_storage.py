from __future__ import annotations

import sqlite3
from pathlib import Path

from aergia._db import initialize


def data_directory(name: str) -> Path:
    return Path.home() / ".local" / "share" / name


def store(name, directory):
    directory.mkdir(exist_ok=True, parents=True)
    db = directory / f"{name}.sqlite"
    with sqlite3.connect(db):
        pass
    return db


def application_db():
    name = "aergia"
    directory = data_directory(name)
    db = store(name, directory)
    initialize(db)
    return db
