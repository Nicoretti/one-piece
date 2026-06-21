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
def ai(log_level: str) -> None:
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


def _prepare() -> None:
    """Ensure the image and persistence volumes are ready before a run."""
    ensure_image()
    ensure_volumes()


@click.command("agent")
@click.argument("tool", type=click.Choice(list(TOOLS)), help="Which registered tool to launch")
@click.argument("path", help="Directory or file path to work on")
@click.argument("args", nargs=-1, help="Additional arguments to pass to the tool")
def agent(tool: str, path: str, args: tuple[str, ...]) -> None:
    """Start a specific AI-agent/tool.

    TOOL is one of: pi, opc (OpenCode), aic (aichat), llm.
    Remaining ARGS are passed straight through to the tool, e.g. ``ai agent pi /path --model x``.
    """
    _prepare()
    spec = TOOLS[tool]
    run_container(
        path,
        [*spec.command, *args],
        include_pi_volume=spec.include_pi_volume,
        workdir_arg=spec.workdir_arg,
    )


@click.command("shell")
@click.argument("path", help="Directory or file path to mount in the container")
def shell(path: str) -> None:
    """Open a shell in the AI container.

    Launch an interactive shell session within the AI container
    for manual command execution and exploration.
    """
    _prepare()
    run_container(path, ["/bin/bash"])


@click.group("image")
def image() -> None:
    """Manage the AI container image."""
    pass


@image.command("rebuild")
def image_rebuild() -> None:
    """Rebuild the container image.

    Running an image rebuild ensures the latest tool versions are
    persistently installed in the container.
    """
    build_image()


ai.add_command(agent)
ai.add_command(shell)
ai.add_command(image)

if __name__ == "__main__":
    ai()
