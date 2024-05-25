from __future__ import annotations

import datetime
import io
import sqlite3
import datetime as dt
from pathlib import Path
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


def save(image: Image, db=None):
    with sqlite3.connect(db) as con:
        with con as transaction:
            stmt = cleandoc("""
            INSERT INTO images (name, model, prompt, revised_prompt, created, blob)
            VALUES (?, ?, ?, ?, ?, ?);
            """)
            result = transaction.execute(
                stmt,
                (
                    image.name,
                    image.model,
                    image.prompt,
                    image.revised_prompt or "[No Revised Prompt]",
                    image.created.timestamp(),
                    image.blob,
                )
            )
        image.id = result.lastrowid
        return image


def load(type, name, db=None) -> Image:
    with sqlite3.connect(db) as con:
        with con as transaction:
            stmt = cleandoc("""
            SELECT id, name, model, prompt, revised_prompt, created, blob FROM images
            WHERE name = ?;
            """)
            result = transaction.execute(stmt, (name,))
            row = result.fetchone()
            names = Image.model_json_schema()['properties'].keys()
            kwargs = dict(zip(names, row))
            kwargs['created'] = datetime.datetime.fromtimestamp(kwargs['created'])
            return Image(**kwargs)


def load_list(type, db=None, limit=10, offset=0):
    with sqlite3.connect(db) as con:
        if limit is None:
            stmt = "SELECT id, name, model, prompt, revised_prompt, created, blob FROM images;"
            result = con.execute(stmt)
        else:
            stmt = cleandoc("""
                SELECT id, name, model, prompt, revised_prompt, created, blob FROM images
                ORDER BY id
                LIMIT ? OFFSET ?;
            """)
            result = con.execute(stmt, (limit, offset))
        names = Image.model_json_schema()['properties'].keys()
        rows = result.fetchall()
        images = []
        for row in rows:
            kwargs = dict(zip(names, row))
            kwargs['created'] = datetime.datetime.fromtimestamp(kwargs['created'])
            images.append(Image(**kwargs))
        return images


def load_blob(type, id, db=None):
    with sqlite3.connect(db) as con:
        stmt = "SELECT blob FROM images WHERE id = ?;"
        result = con.execute(stmt, (id,))
        row = result.fetchone()
        return io.BytesIO(row[0])


TABLES = [Image, Session, Message]


def data_directory(name: str) -> Path:
    return Path.home() / '.local' / 'share' / name


def store(name, directory):
    directory.mkdir(exist_ok=True, parents=True)
    db = directory / f"{name}.sqlite"
    with sqlite3.connect(db) as con:
        pass
    return db


def initialize(db, tables=None):
    tables = tables or []
    with sqlite3.connect(db) as con:
        with con as transaction:
            for table in tables:
                transaction.execute(table.ddl)


def application_db():
    name = 'aergia'
    directory = data_directory(name)
    db = store(name, directory)
    initialize(db, TABLES)
    return db
