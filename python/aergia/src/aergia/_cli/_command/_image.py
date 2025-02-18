import datetime as dt
import io
import sys

import httpx
from PIL import Image as PillowImage
from rich.table import Table
from rich_argparse import ArgumentDefaultsRichHelpFormatter

from aergia._cli._command._utilities import ExitCode
from aergia._client import build_client
from aergia._model._data import Image
from aergia._model._load import load_blob, load_list
from aergia._model._save import save
from aergia._model._storage import application_db


def image(settings, stdout, stderr):
    def download(url, file):
        resp = httpx.get(url)
        file.write(resp.content)

    backend = settings["backend"]
    backend_settings = settings[backend]
    client = build_client(backend=backend, settings=backend_settings)

    if not settings["prompt"]:
        prompt = sys.stdin.read()
    else:
        prompt = settings["prompt"] if isinstance(settings["prompt"], str) else " ".join(settings["prompt"])

    with stdout.status("Generating image ...", spinner="aesthetic", spinner_style="magenta"):
        response = client.images.generate(prompt=prompt, model=settings["model"])
        data = response.data[0]
        image_url = data.url
        revised_prompt = data.revised_prompt
        buffer = io.BytesIO()
        download(image_url, buffer)
        created = dt.datetime.fromtimestamp(response.created)
        img = Image(
            id=None,
            name=settings["name"],
            model=settings["model"],
            prompt=prompt,
            created=created,
            revised_prompt=revised_prompt,
            blob=buffer.getvalue(),
        )
        db = application_db()
        save(img, db)

    pimg = PillowImage.open(buffer)
    pimg.show(settings["name"])

    return ExitCode.Success


def list_images(settings, stdout, stderr):
    table = Table(title="Generated Images")
    table.add_column("Id", justify="right")
    table.add_column("Name", justify="left", style="green")
    table.add_column("Model", justify="left", style="cyan")
    table.add_column("Created", justify="left", style="yellow")
    table.add_column("Prompt", justify="left", style="white")
    table.add_column("Revised-Prompt", justify="left", style="magenta")

    db = application_db()
    limit = None if settings["all"] else settings["limit"]
    images = load_list(Image, db, limit=limit, offset=settings["offset"])
    for img in images:
        table.add_row(
            f"{img.id}",
            img.name,
            img.model,
            f"{img.created}",
            img.prompt,
            img.revised_prompt,
        )

    stdout.print(table)

    return ExitCode.Success


def show_image(settings, stdout, stderr):
    db = application_db()
    blob = load_blob(Image, key="id", value=settings["id"], db=db)
    pimg = PillowImage.open(blob)
    pimg.show()
    return ExitCode.Success


def add_image_subcommand(subparsers):
    # fmt: off
    subcommand = subparsers.add_parser(
        "image",
        help="manage and generate images",
        formatter_class=ArgumentDefaultsRichHelpFormatter,
    )
    sub_subparsers = subcommand.add_subparsers(
        dest="session_subcommand", help="Sessions commands"
    )

    generate_subcommand = sub_subparsers.add_parser(
        "generate",
        help="generate images",
        formatter_class=ArgumentDefaultsRichHelpFormatter,
    )

    generate_subcommand.add_argument(
        "-n",
        "--name",
        type=str,
        default="unnamed",
        help="name or title which will be used for the image",
    )
    generate_subcommand.add_argument(
        "-m",
        "--model",
        default="dall-e-2",
        choices=["dall-e-2", "dall-e-3"],
        help="model to use for generating the image",
    )
    generate_subcommand.add_argument(
        "prompt",
        type=str,
        nargs="*",
        metavar="PROMPT",
        help="prompt which shall be used for generating the image, if None stdin will be read.",
    )
    generate_subcommand.set_defaults(func=image)

    list_subcommand = sub_subparsers.add_parser(
        "list",
        help="list previously generated images",
        formatter_class=ArgumentDefaultsRichHelpFormatter,
    )
    list_subcommand.add_argument(
        "-a", "--all", action="store_true", default=False, help="list all images"
    )
    list_subcommand.add_argument(
        "-l", "--limit", type=int, default=10, help="amount of images to list"
    )
    list_subcommand.add_argument(
        "-o", "--offset", type=int, default=0, help="offset for listing images"
    )
    list_subcommand.set_defaults(func=list_images)

    show_subcommand = sub_subparsers.add_parser(
        "show", help="show an image", formatter_class=ArgumentDefaultsRichHelpFormatter
    )
    show_subcommand.add_argument("id", type=int, help="image to show")
    show_subcommand.set_defaults(func=show_image)
    # fmt: on
    return subcommand
