from __future__ import annotations

import datetime as dt
from pydantic import BaseModel


class Session(BaseModel):
    id: int | None
    name: str
    model: str
    created: dt.datetime
    temperature: float


class Message(BaseModel):
    id: int | None
    content: str
    model: str
    created: dt.datetime
    session_id: int | None


class Image(BaseModel):
    id: int | None
    name: str
    model: str
    prompt: str
    revised_prompt: str | None
    created: dt.datetime
    blob: bytes
