from __future__ import annotations

import datetime as dt
from pydantic import BaseModel


class Session(BaseModel):
    id: int | None
    name: str
    model: str
    temperature: float


class Message(BaseModel):
    id: int | None
    role: str
    content: str
    model: str | None
    session_id: int | None


class Image(BaseModel):
    id: int | None
    name: str
    model: str
    prompt: str
    revised_prompt: str | None
    created: dt.datetime
    blob: bytes
