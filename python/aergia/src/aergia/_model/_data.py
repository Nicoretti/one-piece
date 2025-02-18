from __future__ import annotations

import datetime as dt

from pydantic import BaseModel


class Session(BaseModel):
    id: int | None
    name: str
    model: str
    created: dt.datetime

    @classmethod
    def new(cls, name, model):
        return cls(
            id=None,
            name=name,
            model=model,
            created=dt.datetime.now(),
        )


class Message(BaseModel):
    id: int | None
    content: str
    model: str
    role: str
    created: dt.datetime
    session_id: int | None

    @classmethod
    def user(cls, content, session_id=None):
        return cls(
            id=None,
            content=content,
            model="",
            role="user",
            created=dt.datetime.now(),
            session_id=session_id,
        )

    @classmethod
    def assistant(cls, content, model, session_id=None):
        return cls(
            id=None,
            content=content,
            model=model,
            role="assistant",
            created=dt.datetime.now(),
            session_id=session_id,
        )


class Image(BaseModel):
    id: int | None
    name: str
    model: str
    prompt: str
    revised_prompt: str | None
    created: dt.datetime
    blob: bytes
