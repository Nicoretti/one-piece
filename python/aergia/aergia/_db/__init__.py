import sqlite3
from importlib import resources


def initialize(db):
    sql_file = resources.files(__name__) / "init.sql"
    sql_script = sql_file.read_text()
    with sqlite3.connect(db) as con:
        with con as transaction:
            transaction.executescript(sql_script)
