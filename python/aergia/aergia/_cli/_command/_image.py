import io
import os
import sys
import httpx
import datetime as dt
from openai import OpenAI
from PIL import Image as PillowImage
from rich.table import Table
from rich_argparse import ArgumentDefaultsRichHelpFormatter
from aergia._model._storage import application_db, save, load_list, load_blob
from aergia._model._data import Image
from aergia._cli._command._utilities import ExitCode


def image(args, stdout, stderr):
    def download(url, file):
        resp = httpx.get(url)
        file.write(resp.content)

    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY")
    )
    if not args.prompt:
        prompt = sys.stdin.read()
    else:
        prompt = args.prompt if isinstance(args.prompt, str) else " ".join(args.prompt)
    response = client.images.generate(prompt=prompt, model=args.model)
    data = response.data[0]
    image_url = data.url
    revised_prompt = data.revised_prompt
    buffer = io.BytesIO()
    download(image_url, buffer)
    created = dt.datetime.fromtimestamp(response.created)
    img = Image(
        id=None,
        name=args.name,
        model=args.model,
        prompt=prompt,
        created=created,
        revised_prompt=revised_prompt,
        blob=buffer.getvalue()
    )
    db = application_db()
    save(img, db)

    pimg = PillowImage.open(buffer)
    pimg.show(args.name)

    return ExitCode.Success


def list_images(args, stdout, stderr):
    table = Table(title='Generated Images')
    table.add_column("Id", justify='right')
    table.add_column("Name", justify='left', style='green')
    table.add_column("Model", justify='left', style='cyan')
    table.add_column("Created", justify='left', style='yellow')
    table.add_column("Prompt", justify='left', style='white')
    table.add_column("Revised-Prompt", justify='left', style='magenta')

    db = application_db()
    limit = None if args.all else args.limit
    images = load_list(Image, db, limit=limit, offset=args.offset)
    for img in images:
        table.add_row(
            f"{img.id}",
            img.name,
            img.model,
            f"{img.created}",
            img.prompt,
            img.revised_prompt
        )

    stdout.print(table)

    return ExitCode.Success


def show_image(args, stdout, stderr):
    db = application_db()
    blob = load_blob(Image, args.id, db)
    pimg = PillowImage.open(blob)
    pimg.show()
    return ExitCode.Success


def add_image_subcommand(subparsers):
    subcommand = subparsers.add_parser(
        'image',
        help='manage and generate images',
        formatter_class=ArgumentDefaultsRichHelpFormatter
    )
    sub_subparsers = subcommand.add_subparsers(
        dest='session_subcommand', help='Sessions commands'
    )

    generate_subcommand = sub_subparsers.add_parser(
        'generate',
        help='generate images',
        formatter_class=ArgumentDefaultsRichHelpFormatter
    )

    generate_subcommand.add_argument(
        '-n', '--name', type=str, default='unnamed',
        help='name or title which will be used for the image'
    )
    generate_subcommand.add_argument(
        '-m', '--model',
        default='dall-e-2',
        choices=['dall-e-2', 'dall-e-3'],
        help='model to use for generating the image'
    )
    generate_subcommand.add_argument(
        'prompt', type=str, nargs="*",
        metavar='PROMPT',
        help='prompt which shall be used for generating the image, if None stdin will be read.'
    )
    generate_subcommand.set_defaults(func=image)

    list_subcommand = sub_subparsers.add_parser(
        'list',
        help='list previously generated images',
        formatter_class=ArgumentDefaultsRichHelpFormatter
    )
    list_subcommand.add_argument(
        '-a', '--all', action='store_true', default=False, help='list all images'
    )
    list_subcommand.add_argument(
        '-l', '--limit', type=int, default=10, help='amount of images to list'
    )
    list_subcommand.add_argument(
        '-o', '--offset', type=int, default=0, help='offset for listing images'
    )
    list_subcommand.set_defaults(func=list_images)

    show_subcommand = sub_subparsers.add_parser(
        'show',
        help='show an image',
        formatter_class=ArgumentDefaultsRichHelpFormatter
    )
    show_subcommand.add_argument(
        'id', type=int, help='image to show'
    )
    show_subcommand.set_defaults(func=show_image)
    return subcommand
