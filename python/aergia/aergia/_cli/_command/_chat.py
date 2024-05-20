import os
import asyncio
import argparse
from openai import AsyncOpenAI
from rich.markdown import Markdown
from rich_argparse import ArgumentDefaultsRichHelpFormatter
from aergia._cli._command._utilities import TextBuffer, ExitCode


def chat(args, stdout, stderr):
    async def achat(client, model, message):
        stream = await client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": message}],
            stream=True,
        )
        with stdout.status("Processing request ...", spinner='aesthetic', spinner_style='cyan') as status:
            with TextBuffer() as buffer:
                async for chunk in stream:
                    text = chunk.choices[0].delta.content or ""
                    buffer.append(text)
                content = buffer.content

        stdout.print(
            Markdown(content)
        )
        return ExitCode.Success

    client = AsyncOpenAI(
        api_key=os.environ.get("OPENAI_API_KEY")
    )
    msg = " ".join(args.text)
    context = "" if not args.context else args.context.read()
    msg = msg + context
    return asyncio.run(achat(client=client, model=args.model, message=msg))


def add_chat_subcommand(subparsers):
    subcommand = subparsers.add_parser(
        'chat',
        help='chat with the ai system',
        formatter_class=ArgumentDefaultsRichHelpFormatter
    )
    subcommand.add_argument(
        'text', type=str, nargs=argparse.REMAINDER, help='Text input'
    )
    subcommand.add_argument(
        '-r', '--role', type=str, help='Choose a role'
    )
    subcommand.add_argument(
        '-s', '--session', nargs='?', const=True, help='Create or reuse a session'
    )
    subcommand.add_argument(
        '-c', '--context', type=argparse.FileType('r'), help='File directory or stdin'
    )
    subcommand.add_argument(
        '-m', '--model',
        default='gpt-4o',
        choices=['gpt-4o', 'gpt-4', 'gpt-4-turbo', 'gpt-3.5-turbo'],
        help='Select a model'
    )
    subcommand.add_argument(
        '--stream', dest='stream', action='store_true', default=True, help='Enable streaming'
    )
    subcommand.set_defaults(func=chat)
    return subcommand
