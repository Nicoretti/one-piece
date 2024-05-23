import os
import asyncio
import argparse
from openai import AsyncOpenAI
from rich.markdown import Markdown
from rich_argparse import ArgumentDefaultsRichHelpFormatter
from aergia._cli._command._utilities import TextBuffer, ExitCode
from aergia._client import build_client, Type


def chat(args, stdout, stderr):
    def is_chunk_valid(chunk):
        return chunk.choices is not None and len(chunk.choices) > 0

    async def async_chat(client, model, message):
        stream = await client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": message}],
            stream=True,
        )
        with stdout.status(
            "Processing request ...", spinner="aesthetic", spinner_style="cyan"
        ):
            with TextBuffer() as buffer:
                stream = (c async for c in stream if is_chunk_valid(c))
                async for chunk in stream:
                    text = chunk.choices[0].delta.content or ""
                    buffer.append(text)
                return buffer.content

    def sync_chat(client, model, message):
        stream = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": message}],
            stream=True,
        )
        with stdout.status(
            "Processing request ...", spinner="aesthetic", spinner_style="cyan"
        ):
            with TextBuffer() as buffer:
                stream = (c for c in stream if is_chunk_valid(c))
                for chunk in stream:
                    text = chunk.choices[0].delta.content or ""
                    buffer.append(text)
                return buffer.content

    client_type = Type.Async
    api_key = os.environ.get("OPENAI_API_KEY")
    client = build_client(backend="openai", api_key=api_key, client_type=client_type)
    msg = " ".join(args.text)
    context = "" if not args.context else args.context.read()
    msg = msg + context
    if client_type == Type.Async:
        content = asyncio.run(async_chat(client=client, model=args.model, message=msg))
    else:
        content = sync_chat(client, model=args.model, message=msg)
    stdout.print(Markdown(content))
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
