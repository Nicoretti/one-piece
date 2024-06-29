from __future__ import annotations

import sqlite3
from functools import singledispatch
from inspect import cleandoc

from aergia._model._data import Image, Message, Session


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
            INSERT INTO sessions (name, model, created)
            VALUES (?, ?, ?);
            """)
            result = transaction.execute(
                stmt,
                (session.name, session.model, session.created),
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
