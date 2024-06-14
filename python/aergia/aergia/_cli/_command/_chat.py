import os
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


def chat(args, stdout, stderr):
    def is_chunk_valid(chunk):
        return chunk.choices is not None and len(chunk.choices) > 0

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

    def create_session(name=None):
        name = name or f"Temp-{uuid.uuid4()}"
        try:
            session = load(Session, key="name", value=args.session, db=db)
        except Exception:
            session = Session.new(name, args.model)
            save(session, db)
        return session

    api_key = os.environ.get("OPENAI_API_KEY")
    client = build_client(backend="openai", api_key=api_key, client_type=Type.Sync)
    db = application_db()
    session = create_session(args.session)
    context = "" if not args.context else args.context.read()
    content = " ".join(args.text) + context

    user_msg = Message.user(content, session.id)
    save(user_msg, db)

    messages = list(load(Message, key="session_id", value=session.id, db=db))
    messages = [{"role": m.role, "content": m.content} for m in messages]
    messages.append({"role": user_msg.role, "content": user_msg.content})

    content, model = sync_chat(client, model=args.model, messages=messages)

    assistant_msg = Message.assistant(content, model, session.id)
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
        "-c", "--context", type=argparse.FileType("r"), help="File or stdin (-)"
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
