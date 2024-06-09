import os
import asyncio
import argparse
import uuid
from rich.markdown import Markdown
from rich_argparse import ArgumentDefaultsRichHelpFormatter
from aergia._cli._command._utilities import TextBuffer, ExitCode
from aergia._client import build_client, Type
from aergia._model._save import save
from aergia._model._load import load
from aergia._model._data import Session, Message
from aergia._model._storage import application_db
import datetime


def chat(args, stdout, stderr):
    def is_chunk_valid(chunk):
        return chunk.choices is not None and len(chunk.choices) > 0

    async def async_chat(client, model, messages):
        stream = await client.chat.completions.create(
            model=model,
            messages=messages,
            stream=True,
        )
        with stdout.status(
                "Processing request ...", spinner="aesthetic", spinner_style="cyan"
        ):
            with TextBuffer() as buffer:
                stream = (c async for c in stream if is_chunk_valid(c))
                async for chunk in stream:
                    text = chunk.choices[0].delta.content or ""
                    model = chunk.model
                    buffer.append(text)
                return buffer.content, model

    def sync_chat(client, model, messages):
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            stream=True,
        )
        with stdout.status(
                "Processing request ...", spinner="aesthetic", spinner_style="cyan"
        ):
            with TextBuffer() as buffer:
                stream = (c for c in response if is_chunk_valid(c))
                for chunk in stream:
                    text = chunk.choices[0].delta.content or ""
                    model = chunk.model
                    buffer.append(text)
                return buffer.content, model

    client_type = Type.Async
    api_key = os.environ.get("OPENAI_API_KEY")
    client = build_client(backend="openai", api_key=api_key, client_type=client_type)
    content = " ".join(args.text)
    db = application_db()

    session = args.session or f"Temp-{uuid.uuid4()}"
    if session:
        try:
            session = load(Session, key='name', value=args.session, db=db)
        except Exception:
            session = Session(
                id=None,
                name=session,
                model=args.model,
                created=datetime.datetime.now(),
                temperature=1.0  # FIX: use the actual selected/used temp
            )
            save(session, db)

    context = "" if not args.context else args.context.read()
    content = content + context
    session_id = session.id

    msg = Message(
        id=None,
        content=content,
        model="",
        role="user",
        created=datetime.datetime.now(),
        session_id=session_id
    )
    save(msg, db)

    if args.session:
        messages = list(load(Message, key='session_id', value=session.id, db=db))
        messages = [{"role": m.role, "content": m.content} for m in messages]
    else:
        messages = []

    messages.append({"role": msg.role, "content": msg.content})

    if client_type == Type.Async:
        content, model = asyncio.run(async_chat(client=client, model=args.model, messages=messages))
    else:
        content, model = sync_chat(client, model=args.model, messages=messages)

    assistant_msg = Message(
        id=None,
        content=content,
        model=model,
        role="assistant",
        created=datetime.datetime.now(),
        session_id=session_id,
    )
    save(assistant_msg, db)

    stdout.print(Markdown(assistant_msg.content))
    return ExitCode.Success


def add_chat_subcommand(subparsers):
    subcommand = subparsers.add_parser(
        "chat",
        help="chat with the ai system",
        formatter_class=ArgumentDefaultsRichHelpFormatter,
    )
    subcommand.add_argument(
        "text", type=str, nargs=argparse.REMAINDER, help="Text input"
    )
    subcommand.add_argument("-r", "--role", type=str, help="Choose a role")
    subcommand.add_argument(
        "-s", "--session", nargs="?", const=True, help="Create or reuse a session"
    )
    subcommand.add_argument(
        "-c", "--context", type=argparse.FileType("r"), help="File directory or stdin"
    )
    subcommand.add_argument(
        "-m",
        "--model",
        default="gpt-4o",
        choices=["gpt-4o", "gpt-4", "gpt-4-turbo", "gpt-3.5-turbo"],
        help="Select a model",
    )
    subcommand.set_defaults(func=chat)
    return subcommand
