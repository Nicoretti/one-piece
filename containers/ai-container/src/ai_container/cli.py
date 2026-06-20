import logging

import rich_click as click
from rich.logging import RichHandler

from ai_container._podman import (
    build_image,
    ensure_image,
    ensure_volumes,
    run_container,
)


def _configure_logging() -> None:
    """Route library log records to the console via rich."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(show_path=False, rich_tracebacks=True)],
    )


@click.group()
def ai() -> None:
    """AI Container Command Tools.

    A unified interface for running various AI coding agents and tools
    within an isolated container. Supports PI, OpenCode, aichat, and llm commands.

    Podman setup (image build, volume creation) is handled through the
    Podman SDK.
    """
    _configure_logging()


def _prepare(*, rebuild_image: bool) -> None:
    """Ensure the image and persistence volumes are ready before a run."""
    ensure_image(rebuild=rebuild_image)
    ensure_volumes()


@click.command("pi")
@click.argument("path")
@click.argument("args", nargs=-1)
@click.option("--rebuild-image", is_flag=True, help="Rebuild the container image before running.")
def run_pi(path: str, args: tuple[str, ...], rebuild_image: bool = False) -> None:
    """Run PI coding agent.

    PI is a powerful coding agent that helps with code generation,
    analysis, and refactoring tasks within containers.

    Args:
        path: Directory or file path to work on.
        args: Additional arguments to pass to PI.
        rebuild_image: If set, rebuild the container image before running.
    """
    _prepare(rebuild_image=rebuild_image)
    run_container(path, ["pi", *args])


@click.command("opc")
@click.argument("path")
@click.argument("args", nargs=-1)
@click.option("--rebuild-image", is_flag=True, help="Rebuild the container image before running.")
def run_opc(path: str, args: tuple[str, ...], rebuild_image: bool = False) -> None:
    """Run OpenCode coding agent.

    OpenCode is an AI-powered coding assistant designed for
    enterprise development environments.

    Args:
        path: Directory or file path to work on.
        args: Additional arguments to pass to OpenCode.
        rebuild_image: If set, rebuild the container image before running.
    """
    _prepare(rebuild_image=rebuild_image)
    run_container(path, ["opencode", *args], include_pi_volume=False, workdir_arg=True)


@click.command("aic")
@click.argument("path")
@click.argument("args", nargs=-1)
@click.option("--rebuild-image", is_flag=True, help="Rebuild the container image before running.")
def run_aic(path: str, args: tuple[str, ...], rebuild_image: bool = False) -> None:
    """Run aichat/aichat-command.

    AIChat is an interactive AI chat interface for code assistance
    and general programming queries.

    Args:
        path: Directory or file path to work on.
        args: Additional arguments to pass to AIChat.
        rebuild_image: If set, rebuild the container image before running.
    """
    _prepare(rebuild_image=rebuild_image)
    run_container(path, ["aichat", *args], include_pi_volume=False)


@click.command("llm")
@click.argument("path")
@click.argument("args", nargs=-1)
@click.option("--rebuild-image", is_flag=True, help="Rebuild the container image before running.")
def run_llm(path: str, args: tuple[str, ...], rebuild_image: bool = False) -> None:
    """Run llm/llm-command.

    LLM is a command-line tool for interacting with large language models
    and performing AI-powered text operations.

    Args:
        path: Directory or file path to work on.
        args: Additional arguments to pass to LLM.
        rebuild_image: If set, rebuild the container image before running.
    """
    _prepare(rebuild_image=rebuild_image)
    run_container(path, ["uvx", "llm", *args], include_pi_volume=False)


@click.command("shell")
@click.argument("path")
@click.option("--rebuild-image", is_flag=True, help="Rebuild the container image before running.")
def shell(path: str, rebuild_image: bool = False) -> None:
    """Open a shell in the AI container.

    Launch an interactive shell session within the AI container
    for manual command execution and exploration.

    Args:
        path: Directory or file path to mount in the container.
        rebuild_image: If set, rebuild the container image before running.
    """
    _prepare(rebuild_image=rebuild_image)
    run_container(path, ["/bin/bash"])


@click.command("rebuild-image")
def rebuild_image() -> None:
    """Rebuilds the container image.

    Running an image rebuild ensures the latest tool versions are
    persistently installed in the container.
    """
    build_image()


ai.add_command(run_pi)
ai.add_command(run_opc)
ai.add_command(run_aic)
ai.add_command(run_llm)
ai.add_command(shell)
ai.add_command(rebuild_image)

if __name__ == "__main__":
    ai()
