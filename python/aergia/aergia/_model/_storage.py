from __future__ import annotations
from typing import Any
import datetime
import io
import sqlite3
from pathlib import Path
from inspect import cleandoc
from importlib import resources
from functools import singledispatch

from class_singledispatch import class_singledispatch

from aergia._model._data import Session, Image, Message
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


@singledispatch
def save(type, db=None):
    raise TypeError(f"Type {type.__class__}, is not supported yet.")


@save.register
def _(image: Image, db=None):
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
                    image.revised_prompt or "<NO-REVISED-PROMPT>",
                    image.created.timestamp(),
                    image.blob,
                ),
            )
        image.id = result.lastrowid
        return image


@save.register
def _(session: Session, db=None):
    with sqlite3.connect(db) as con:
        with con as transaction:
            stmt = cleandoc("""
            INSERT INTO sessions (name, model, created, temperature)
            VALUES (?, ?, ?, ?);
            """)
            result = transaction.execute(
                stmt,
                (session.name, session.model, session.created, session.temperature),
            )
        session.id = result.lastrowid
        return session

@save.register
def _(message: Message, db=None):
    with sqlite3.connect(db) as con:
        with con as transaction:
            stmt = cleandoc("""
            INSERT INTO messages (content, model, role, created, session_id)
            VALUES (?, ?, ?, ?, ?);
            """)
            result = transaction.execute(
                stmt,
                (message.content, message.model, message.role, message.created, message.session_id),
            )
        message.id = result.lastrowid
        return message


@class_singledispatch
def load(type: type[Any], key, value, db=None):
    raise TypeError(f"Type {type}, is not supported yet.")


@load.register
def _(image: type[Image], key, value, db):
    with sqlite3.connect(db) as con:
        with con as transaction:
            stmt = cleandoc(f"""
            SELECT id, name, model, prompt, revised_prompt, created, blob FROM images
            WHERE {key} = ?;
            """)
            result = transaction.execute(stmt, (value,))
            row = result.fetchone()
            names = image.model_json_schema()["properties"].keys()
            kwargs = dict(zip(names, row))
            kwargs["created"] = datetime.datetime.fromtimestamp(kwargs["created"])
            return Image(**kwargs)


@load.register
def _(session: type[Session], key, value, db):
    with sqlite3.connect(db) as con:
        with con as transaction:
            stmt = cleandoc(f"""
            SELECT id, name, model, created, temperature FROM sessions
            WHERE {key} = ?;
            """)
            result = transaction.execute(stmt, (value,))
            row = result.fetchone()
            names = session.model_json_schema()["properties"].keys()
            kwargs = dict(zip(names, row))
            return Session(**kwargs)

@load.register
def _(message: type[Message], key, value, db):
    with sqlite3.connect(db) as con:
        with con as transaction:
            stmt = cleandoc(f"""
            SELECT id, content, model, role, created, session_id FROM messages
            WHERE {key} = ?;
            """)
            result = transaction.execute(stmt, (value,))
            for row in result:
                names = message.model_json_schema()["properties"].keys()
                kwargs = dict(zip(names, row))
                yield Message(**kwargs)


@class_singledispatch
def load_list(type: type[Any], db=None, limit=10, offset=0):
    raise TypeError(f"Type {type}, is not supported yet.")


@load_list.register
def _(image: type[Image], db=None, limit=10, offset=0):
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
        names = Image.model_json_schema()["properties"].keys()
        rows = result.fetchall()
        images = []
        for row in rows:
            kwargs = dict(zip(names, row))
            kwargs["created"] = datetime.datetime.fromtimestamp(kwargs["created"])
            images.append(Image(**kwargs))
        return images


@class_singledispatch
def load_blob(type: type[Any], id, db=None):
    raise TypeError(f"Type {type}, is not supported yet.")


@load_blob.register
def _(image: type[Image], key, value, db=None):
    with sqlite3.connect(db) as con:
        stmt = f"SELECT blob FROM images WHERE {key} = ?;"
        result = con.execute(stmt, (value,))
        row = result.fetchone()
        return io.BytesIO(row[0])
