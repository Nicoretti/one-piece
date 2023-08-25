import sys
import datetime

import typer
from enum import Enum
from rich import print
from end_of_life import api

CLI = typer.Typer(name="eol")


class Status(Enum):
    Info = "End of life will be in more than 6 months"
    Warning = "End of life will be in less than siz months"
    Failure = "End of life is already reached"


def _status(date) -> Status:
    today = datetime.date.today()
    diff = date - today
    if diff.days <= 0:
        return Status.Failure
    if diff.days <= 180:
        return Status.Warning
    return Status.Info


@CLI.command(name="check")
def eol(product: str, version: str, warnings_as_error: bool = False, silent: bool = False):
    """Check if a product already reached its end of life."""
    product = product.lower()
    info = api.product_cycle_details(product, version)
    status = _status(info.eol)
    is_eol = status == Status.Failure or (warnings_as_error and status == Status.Warning)
    color = {Status.Info: "green", Status.Warning: "yellow", Status.Failure: "red"}
    message = {
        False: "[{color}]Success, {product}: {version} did not reach it's End-Of-Life yet.[/{color}]",
        True: "[{color}]Failure, {product}: {version} already reached it's End-Of-Life.[/{color}]"
    }[is_eol]
    if not silent:
        print(message.format(product=product, version=version, color=color[status]))
    exit_code = 0 if not is_eol else -1
    sys.exit(exit_code)


@CLI.command(name="list")
def list(include_versions: bool = False):
    """List all products which are available."""
    for p in api.all_products():
        print(p)
    sys.exit(0)


# add check if requested product is supported
@CLI.command(name="info")
def info(product: str, version: str = None):
    """Get detailed information about a specific product."""
    info = api.product_details(product) if version is None else [api.product_cycle_details(product, version)]
    for p in info:
        print(p)
    sys.exit(0)


@CLI.command(name="versions")
def versions(product: str):
    """List all available versions of a product."""
    version_info = api.product_versions(product)
    for version in version_info:
        print(f"{version}")
    sys.exit(0)


def main():
    CLI()


if __name__ == '__main__':
    main()
