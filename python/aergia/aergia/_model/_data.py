from __future__ import annotations

import datetime as dt
from inspect import cleandoc

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
    id: int | None
    name: str
    model: str
    prompt: str
    revised_prompt: str | None
    created: dt.datetime
    blob: bytes

    @classmethod
    @property
    def ddl(cls):
        return cleandoc(f"""
        CREATE TABLE  IF NOT EXISTS {cls._TABLE_NAME.default} (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            model TEXT NOT NULL,
            prompt TEXT NOT NULL,
            revised_prompt TEXT NOT NULL,
            created INTEGER NOT NULL, 
            blob BLOB NOT NULL
        );
        """)
