from __future__ import annotations

import datetime
import io
import sqlite3
from inspect import cleandoc

from class_singledispatch import class_singledispatch

from aergia._model._data import Image, Message, Session


@class_singledispatch
def load(type: type[object], key, value, db=None):
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
            SELECT id, name, model, created FROM sessions
            WHERE {key} = ?;
            """)
            result = transaction.execute(stmt, (value,))
            row = result.fetchone()
            if not row:
                raise Exception("Session not found.")
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
def load_list(type: type[object], db=None, limit=10, offset=0):
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


@load_list.register
def _(image: type[Session], db=None, limit=10, offset=0):
    with sqlite3.connect(db) as con:
        if limit is None:
            stmt = "SELECT id, name, model, created FROM sessions;"
            result = con.execute(stmt)
        else:
            stmt = cleandoc("""
                SELECT id, name, model, created FROM sessions
                ORDER BY id
                LIMIT ? OFFSET ?;
            """)
            result = con.execute(stmt, (limit, offset))
        names = Session.model_json_schema()["properties"].keys()
        rows = result.fetchall()
        sessions = []
        for row in rows:
            kwargs = dict(zip(names, row))
            sessions.append(Session(**kwargs))
        return sessions


@class_singledispatch
def load_blob(type: type[object], id, db=None):
    raise TypeError(f"Type {type}, is not supported yet.")


@load_blob.register
def _(image: type[Image], key, value, db=None):
    with sqlite3.connect(db) as con:
        stmt = f"SELECT blob FROM images WHERE {key} = ?;"
        result = con.execute(stmt, (value,))
        row = result.fetchone()
        return io.BytesIO(row[0])
