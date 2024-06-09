from __future__ import annotations
import sqlite3
from pathlib import Path
from importlib import resources
from aergia import _db


def data_directory(name: str) -> Path:
    return Path.home() / ".local" / "share" / name


def store(name, directory):
    directory.mkdir(exist_ok=True, parents=True)
    db = directory / f"{name}.sqlite"
    with sqlite3.connect(db):
        pass
    return db


def initialize(db):
    sql_file = resources.files(_db) / "init.sql"
    sql_script = sql_file.read_text()
    with sqlite3.connect(db) as con:
        with con as transaction:
            transaction.executescript(sql_script)


def application_db():
    name = "aergia"
    directory = data_directory(name)
    db = store(name, directory)
    initialize(db)
    return db


