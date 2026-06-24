import logging
import os
import subprocess
from dataclasses import dataclass

import rich_click as click
from rich.console import Console
from rich.logging import RichHandler

from ai_container._podman import (
    BASE_ENV,
    build_image,
    create_environment,
    ensure_image,
    ensure_volumes,
    environment_context,
    environment_exists,
    environments_dir,
    image_exists,
    list_environments,
    remove_environment,
    run_container,
)

LOG_LEVELS = ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")

stdout = Console()


@dataclass(frozen=True)
class RunContext:
    """State shared across commands via the Click context.

    Attributes:
        env: The selected environment (image ``aic:<env>``).
        dryrun: Whether to print podman commands instead of executing them.
    """

    env: str
    dryrun: bool


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
    "claude": Tool(("claude",)),
    "aic": Tool(("aichat",)),
    "llm": Tool(("uvx", "llm")),
}


@click.group()
@click.option(
    "--env",
    "-e",
    "env_name",
    default=BASE_ENV,
    show_default=True,
    help="Which environment (customized image) to use.",
)
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
def ai(ctx: click.Context, env_name: str, log_level: str, dryrun: bool) -> None:
    """AI Container Command Tool.

    A unified interface for running AI coding agents and tools within a container.
    Use ``ai agent <tool> <path> [args]`` to invoke a tool, ``ai shell <path>`` for an
    interactive shell, ``ai env`` to manage custom environments, or
    ``ai image rebuild`` to refresh the container image. Select an environment with
    ``-e/--env`` (e.g. ``ai -e rust shell .``).
    """
    logging.basicConfig(
        level=log_level.upper(),
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(console=Console(stderr=True), rich_tracebacks=True)],
    )
    ctx.obj = RunContext(env=env_name, dryrun=dryrun)


def _resolve_env(env: str) -> str:
    """Validate that an environment exists, aborting with a helpful message."""
    if not environment_exists(env):
        raise click.UsageError(
            f"Unknown environment '{env}'.\n"
            f"Create it with 'ai env new {env}' or list existing ones with 'ai env list'."
        )
    return env


def _prepare(ctx: RunContext) -> None:
    """Ensure the image and persistence volumes are ready before a run."""
    _resolve_env(ctx.env)
    ensure_image(ctx.env, dryrun=ctx.dryrun)
    ensure_volumes(dryrun=ctx.dryrun)


@click.command("agent")
@click.argument("tool", type=click.Choice(list(TOOLS)), help="Which registered tool to launch")
@click.argument("path", help="Directory or file path to work on")
@click.argument("args", nargs=-1, help="Additional arguments to pass to the tool")
@click.pass_obj
def agent(ctx: RunContext, tool: str, path: str, args: tuple[str, ...]) -> None:
    """Start a specific AI-agent/tool.

    TOOL is one of: pi, opc (OpenCode), claude, aic (aichat), llm.
    Remaining ARGS are passed straight through to the tool, e.g. ``ai agent pi /path --model x``.
    """
    _prepare(ctx)
    spec = TOOLS[tool]
    run_container(
        path,
        [*spec.command, *args],
        env=ctx.env,
        include_pi_volume=spec.include_pi_volume,
        workdir_arg=spec.workdir_arg,
        dryrun=ctx.dryrun,
    )


@click.command("shell")
@click.argument("path", help="Directory or file path to mount in the container")
@click.pass_obj
def shell(ctx: RunContext, path: str) -> None:
    """Open a shell in the AI container.

    Launch an interactive shell session within the AI container
    for manual command execution and exploration.
    """
    _prepare(ctx)
    run_container(path, ["/bin/bash"], env=ctx.env, dryrun=ctx.dryrun)


@click.group("image")
def image() -> None:
    """Manage the AI container image."""
    pass


@image.command("rebuild")
@click.pass_obj
def image_rebuild(ctx: RunContext) -> None:
    """Rebuild the container image for the selected environment.

    Running an image rebuild ensures the latest tool versions are
    persistently installed in the container. Non-base environments are rebuilt
    ``FROM aic:base``; pass ``-e base`` (the default) to rebuild the base image.
    """
    _resolve_env(ctx.env)
    if ctx.env != BASE_ENV:
        ensure_image(BASE_ENV, dryrun=ctx.dryrun)
    build_image(ctx.env, dryrun=ctx.dryrun)


@click.group("env")
def env() -> None:
    """Manage custom environments (customized images)."""
    pass


@env.command("list")
def env_list() -> None:
    """List available environments and whether their image is built."""
    for name in list_environments():
        built = "built" if image_exists(name) else "not built"
        stdout.print(f"{name}  [{built}]")


@env.command("new")
@click.argument("name", help="Name of the environment to create")
@click.option("--edit", "open_editor", is_flag=True, help="Open the new Containerfile in $EDITOR.")
def env_new(name: str, open_editor: bool) -> None:
    """Scaffold a new environment definition.

    Creates ``environments/<name>/Containerfile`` (extending ``aic:base``) under
    the user config directory. Build it on first use or with ``ai -e <name> image rebuild``.
    """
    try:
        containerfile = create_environment(name)
    except ValueError as exc:
        raise click.UsageError(str(exc)) from exc
    stdout.print(f"Created environment '{name}' at {containerfile}")
    if open_editor:
        _open_in_editor(containerfile)


@env.command("edit")
@click.argument("name", help="Name of the environment to edit")
def env_edit(name: str) -> None:
    """Open an environment's Containerfile in $EDITOR."""
    if not environment_exists(name) or name == BASE_ENV:
        raise click.UsageError(
            f"Unknown environment '{name}'. Create it with 'ai env new {name}'."
        )
    _open_in_editor(environment_context(name) / "Containerfile")


@env.command("remove")
@click.argument("name", help="Name of the environment to remove")
@click.option("--purge", is_flag=True, help="Also remove the built image.")
@click.pass_obj
def env_remove(ctx: RunContext, name: str, purge: bool) -> None:
    """Delete an environment definition (and optionally its image)."""
    try:
        remove_environment(name, purge=purge, dryrun=ctx.dryrun)
    except ValueError as exc:
        raise click.UsageError(str(exc)) from exc
    stdout.print(f"Removed environment '{name}'.")


@env.command("path")
@click.argument("name", required=False, help="Optional environment name")
def env_path(name: str | None) -> None:
    """Print the environments directory, or a specific definition path."""
    if name is None:
        stdout.print(str(environments_dir()))
        return
    if not environment_exists(name) or name == BASE_ENV:
        raise click.UsageError(f"Unknown environment '{name}'.")
    stdout.print(str(environment_context(name) / "Containerfile"))


def _open_in_editor(path) -> None:
    """Open ``path`` in the user's ``$EDITOR`` (defaults to ``vi``)."""
    editor = os.environ.get("EDITOR", "vi")
    subprocess.run([editor, str(path)])


ai.add_command(agent)
ai.add_command(shell)
ai.add_command(image)
ai.add_command(env)

if __name__ == "__main__":
    ai()
