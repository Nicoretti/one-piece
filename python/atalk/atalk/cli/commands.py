import asyncio
import io
import os
from rich.table import Table
from inspect import cleandoc

import httpx
from openai import AsyncOpenAI, OpenAI
from rich.markdown import Markdown

from enum import IntEnum


class ExitCode(IntEnum):
    Success = 0
    Failure = 1


class TextBuffer:
    """Class to manage a text buffer using StringIO."""

    def __init__(self):
        """
        Initializes a new instance of the TextBuffer class.
        """
        self._buffer = io.StringIO()

    def __enter__(self):
        """
        Enters the runtime context related to this object.

        Returns:
            The TextBuffer instance.
        """
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Exits the runtime context related to this object.

        Args:
            exc_type: The exception type.
            exc_val: The exception value.
            exc_tb: The traceback object.
        """
        self._buffer.close()

    def append(self, text):
        """
        Appends text to the buffer.

        Args:
            text: The text to append to the buffer.
        """
        self._buffer.write(text)

    def __iadd__(self, other):
        """
        Implements the in-place addition operation.

        Args:
            other: The text to add to the buffer.

        Returns:
            The TextBuffer instance.
        """
        self._buffer.write(other)
        return self

    @property
    def content(self):
        """
        Retrieves the content of the buffer.

        Returns:
            The content of the buffer as a string.
        """
        return self._buffer.getvalue()


def default(args, stdout, stderr):
    err_msg = cleandoc(f"""
    This function is not implemented yet!
        
        Details:
            Args: {args}
            
        In case you need more details, consider running the command with the `--debug` flag.
    """)
    raise NotImplementedError(err_msg)


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


def image(args, stdout, stderr):
    def download(url, file_name):
        resp = httpx.get(url)
        with open(file_name, 'wb') as f:
            f.write(resp.content)

    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY")
    )
    prompt = " ".join(args.text)
    response = client.images.generate(prompt=prompt, model=args.model)
    image_url = response.data[0].url
    download(image_url, args.filename)

    return ExitCode.Success


def models(args, stdout, stderr):
    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY")
    )
    models = client.models.list()

    table = Table(title='Available Models of Backend')
    table.add_column("Id/Name", justify='left', style='green')
    table.add_column("Owned By", justify='left', style='cyan')
    table.add_column("Created", justify='left', style='yellow')

    import datetime
    for m in models:
        created = f"{datetime.datetime.fromtimestamp(m.created)}"
        table.add_row(m.id, m.owned_by, created)

    stdout.print(table)

    return ExitCode.Success
