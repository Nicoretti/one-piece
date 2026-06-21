import logging
from dataclasses import dataclass

import rich_click as click
from rich.console import Console
from rich.logging import RichHandler

from ai_container._podman import (
    build_image,
    ensure_image,
    ensure_volumes,
    run_container,
)

LOG_LEVELS = ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")


@dataclass(frozen=True)
class Tool:
    """How a single AI tool is launched inside the container.

    Attributes:
        command: The base command (and fixed args) to run in the container.
        include_pi_volume: Whether to mount the ``pi-config`` volume.
        workdir_arg: If True, append ``.`` after the command (used by opencode).
    """

    command: tuple[str, ...]
    include_pi_volume: bool = False
    workdir_arg: bool = False


# Registry of supported tools, keyed by the name passed to ``ai agent``.
TOOLS = {
    "pi": Tool(("pi",), include_pi_volume=True),
    "opc": Tool(("opencode",), workdir_arg=True),
    "aic": Tool(("aichat",)),
    "llm": Tool(("uvx", "llm")),
}


@click.group()
@click.option(
    "--log-level",
    type=click.Choice(LOG_LEVELS, case_sensitive=False),
    default="INFO",
    show_default=True,
    help="Set the logging verbosity.",
)
@click.option(
    "--dryrun",
    is_flag=True,
    help="Print the podman commands that would run instead of executing them.",
)
@click.pass_context
def ai(ctx: click.Context, log_level: str, dryrun: bool) -> None:
    """AI Container Command Tool.

    A unified interface for running AI coding agents and tools within a container. 
    Use ``ai agent <tool> <path> [args]`` to invoke a tool, ``ai shell <path>`` for an interactive shell
    or ``ai image rebuild`` to refresh the contaier image.
    """
    logging.basicConfig(
        level=log_level.upper(),
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(console=Console(stderr=True), rich_tracebacks=True)],
    )
    ctx.obj = dryrun


def _prepare(*, dryrun: bool = False) -> None:
    """Ensure the image and persistence volumes are ready before a run."""
    ensure_image(dryrun=dryrun)
    ensure_volumes(dryrun=dryrun)


@click.command("agent")
@click.argument("tool", type=click.Choice(list(TOOLS)), help="Which registered tool to launch")
@click.argument("path", help="Directory or file path to work on")
@click.argument("args", nargs=-1, help="Additional arguments to pass to the tool")
@click.pass_obj
def agent(dryrun: bool, tool: str, path: str, args: tuple[str, ...]) -> None:
    """Start a specific AI-agent/tool.

    TOOL is one of: pi, opc (OpenCode), aic (aichat), llm.
    Remaining ARGS are passed straight through to the tool, e.g. ``ai agent pi /path --model x``.
    """
    _prepare(dryrun=dryrun)
    spec = TOOLS[tool]
    run_container(
        path,
        [*spec.command, *args],
        include_pi_volume=spec.include_pi_volume,
        workdir_arg=spec.workdir_arg,
        dryrun=dryrun,
    )


@click.command("shell")
@click.argument("path", help="Directory or file path to mount in the container")
@click.pass_obj
def shell(dryrun: bool, path: str) -> None:
    """Open a shell in the AI container.

    Launch an interactive shell session within the AI container
    for manual command execution and exploration.
    """
    _prepare(dryrun=dryrun)
    run_container(path, ["/bin/bash"], dryrun=dryrun)


@click.group("image")
def image() -> None:
    """Manage the AI container image."""
    pass


@image.command("rebuild")
@click.pass_obj
def image_rebuild(dryrun: bool) -> None:
    """Rebuild the container image.

    Running an image rebuild ensures the latest tool versions are
    persistently installed in the container.
    """
    build_image(dryrun=dryrun)


ai.add_command(agent)
ai.add_command(shell)
ai.add_command(image)

if __name__ == "__main__":
    ai()
