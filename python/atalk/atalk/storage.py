from __future__ import annotations

import sqlite3
from pathlib import Path
from inspect import cleandoc
from contextlib import contextmanager

from pydantic import BaseModel


class Session:
    _TABLE_NAME = 'session'

    id: int
    name: str
    model: str
    temperature: float

    @classmethod
    @property
    def ddl(cls):
        return cleandoc(f"""
        CREATE TABLE IF NOT EXISTS {cls._TABLE_NAME} (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL UNIQUE,
            model TEXT NOT NULL,
            temperature REAL NOT NULL
        );
        """)


class Message:
    _TABLE_NAME = 'messages'

    id: int
    role: str
    content: str
    session_id: int

    @classmethod
    @property
    def ddl(cls):
        return cleandoc(f"""
        CREATE TABLE IF NOT EXISTS {cls._TABLE_NAME} (
            id INTEGER PRIMARY KEY,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            session_id INTEGER,
            FOREIGN KEY (session_id) REFERENCES sessions(id)
        );
        """)


class Image(BaseModel):
    _TABLE_NAME = 'images'
    name: str
    data: bytes

    @classmethod
    @property
    def ddl(cls):
        return cleandoc(f"""
        CREATE TABLE  IF NOT EXISTS {cls._TABLE_NAME.default} (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            blob BLOB NOT NULL
        );
        """)


TABLES = [Image, Session, Message]


def application_data_dir(name: str) -> Path:
    return Path.home() / '.local' / 'share' / name


def application_db(name: str) -> Path:
    return application_data_dir(name) / f"{name}.sqlite"


@contextmanager
def store(name):
    data_dir = application_data_dir(name)
    data_dir.mkdir(exist_ok=True, parents=True)
    db = application_db(name)
    with sqlite3.connect(db) as con:
        yield con


@contextmanager
def db(name, tables):
    with store(name) as con:
        for table in tables:
            con.execute(table.ddl)
        yield con
