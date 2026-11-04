import logging
import os
import subprocess
from dataclasses import dataclass

import rich_click as click
from click.core import ParameterSource
from rich.console import Console
from rich.logging import RichHandler

from ai_container._config import ConfigError, load_config
from ai_container._podman import (
    BASE_ENV,
    create_environment,
    ensure_image,
    ensure_images,
    ensure_volumes,
    environment_context,
    environment_exists,
    environments_dir,
    image_exists,
    list_environments,
    parent_of,
    remove_environment,
    run_container,
)

LOG_LEVELS = ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")

log = logging.getLogger(__name__)
stdout = Console()


@dataclass(frozen=True)
class Context:
    """State shared across commands via the Click context.

    Attributes:
        default_env: Environment used when a command gets no ``-e/--env``.
        dryrun: Whether to print podman commands instead of executing them.
    """

    default_env: str
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


# Shared ``-e/--env`` option for commands that run or build an environment.
env_option = click.option(
    "--env",
    "-e",
    "env_name",
    default=None,
    help="Which environment (customized image) to use. [config: env]",
)


@click.group()
@click.option(
    "--log-level",
    type=click.Choice(LOG_LEVELS, case_sensitive=False),
    default=None,
    help="Set the logging verbosity. [config: log_level]",
)
@click.option(
    "--dryrun",
    default=None,
    is_flag=True,
    help="Print the podman commands that would run instead of executing them.",
)
@click.pass_context
def ai(
    ctx: click.Context,
    log_level: str | None,
    dryrun: bool | None,
) -> None:
    """AI Container Command Tool.

    A unified interface for running AI coding agents and tools within a container.
    Use ``ai agent <tool> <path> [args]`` to invoke a tool, ``ai shell <path>`` for an
    interactive shell, ``ai env`` to manage custom environments, or
    ``ai image rebuild`` to refresh the container image. Select an environment per
    command with ``-e/--env`` (e.g. ``ai shell -e rust .``).

    Defaults come from config files (``.ai-container.toml`` in the project,
    ``~/.config/ai-container/config.toml``, or ``~/.ai-container.toml``); flags
    override them.
    """
    # Configure logging up front (CLI flag, else INFO) so config-loading debug
    # output is visible; the level is refreshed once the config resolves it.
    logging.basicConfig(
        level=(log_level or "INFO").upper(),
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(console=Console(stderr=True), rich_tracebacks=True)],
    )
    try:
        config = load_config()
    except ConfigError as exc:
        raise click.UsageError(str(exc)) from exc
    log_level = _resolve_option(ctx, "log_level", log_level, config["log_level"])
    dryrun = _resolve_option(ctx, "dryrun", dryrun, config["dryrun"])
    logging.getLogger().setLevel(log_level.upper())
    ctx.obj = Context(default_env=config["env"], dryrun=dryrun)


def _resolve_option(ctx: click.Context, name: str, value, fallback):
    """Return the flag value if the user passed it, else the config fallback."""
    if ctx.get_parameter_source(name) is ParameterSource.COMMANDLINE:
        log.debug("Option '%s' from command line: %r", name, value)
        return value
    log.debug("Option '%s' from config/default: %r", name, fallback)
    return fallback


def _resolve_env(ctx: Context, env_name: str | None) -> str:
    """Pick the command's environment (flag, else config) and validate it exists."""
    env = env_name or ctx.default_env
    log.debug("Using environment %r", env)
    if not environment_exists(env):
        raise click.UsageError(
            f"Unknown environment '{env}'.\n"
            f"Create it with 'ai env new {env}' or list existing ones with 'ai env list'."
        )
    return env


def _prepare(ctx: Context, env_name: str | None) -> str:
    """Ensure the image and persistence volumes are ready before a run.

    Returns:
        The resolved environment name.
    """
    env = _resolve_env(ctx, env_name)
    try:
        ensure_image(env, dryrun=ctx.dryrun)
    except ValueError as exc:
        raise click.UsageError(str(exc)) from exc
    ensure_volumes(dryrun=ctx.dryrun)
    return env


@click.command(
    "agent",
    # Options must precede TOOL; everything after it is passed to the tool.
    context_settings={"ignore_unknown_options": True, "allow_interspersed_args": False},
)
@click.argument("tool", type=click.Choice(list(TOOLS)), help="Which registered tool to launch")
@click.argument("path", help="Directory or file path to work on")
@click.argument("args", nargs=-1, help="Additional arguments to pass to the tool")
@env_option
@click.pass_obj
def agent(
    ctx: Context, tool: str, path: str, args: tuple[str, ...], env_name: str | None
) -> None:
    """Start a specific AI-agent/tool.

    TOOL is one of: pi, opc (OpenCode), claude, aic (aichat), llm.
    Remaining ARGS are passed straight through to the tool, e.g. ``ai agent pi /path --model x``.
    Select the environment with ``-e/--env`` before the tool, e.g. ``ai agent -e rust pi .``.
    """
    env = _prepare(ctx, env_name)
    spec = TOOLS[tool]
    run_container(
        path,
        [*spec.command, *args],
        env=env,
        include_pi_volume=spec.include_pi_volume,
        workdir_arg=spec.workdir_arg,
        dryrun=ctx.dryrun,
    )


@click.command("shell")
@click.argument("path", help="Directory or file path to mount in the container")
@env_option
@click.pass_obj
def shell(ctx: Context, path: str, env_name: str | None) -> None:
    """Open a shell in the AI container.

    Launch an interactive shell session within the AI container
    for manual command execution and exploration.
    """
    env = _prepare(ctx, env_name)
    run_container(path, ["/bin/bash"], env=env, dryrun=ctx.dryrun)


@click.group("image")
def image() -> None:
    """Manage the AI container image."""


def _split_names(
    ctx: click.Context, param: click.Parameter, values: tuple[str, ...]
) -> tuple[str, ...]:
    """Flatten arguments so ``pi,pi-python rust`` yields ``pi``, ``pi-python``, ``rust``."""
    names = (name.strip() for value in values for name in value.split(","))
    return tuple(name for name in names if name)


def _complete_names(
    ctx: click.Context, param: click.Parameter, incomplete: str
) -> list[str]:
    """Shell-complete image/environment names (built-in and user-defined)."""
    return [name for name in list_environments() if name.startswith(incomplete)]


@image.command("rebuild")
@click.argument(
    "names",
    nargs=-1,
    callback=_split_names,
    shell_complete=_complete_names,
    help="Images/environments to rebuild, space- or comma-separated [default: config env]",
)
@click.option(
    "--all",
    "rebuild_all",
    is_flag=True,
    help="Rebuild every image (built-in and user environments).",
)
@click.pass_obj
def image_rebuild(ctx: Context, names: tuple[str, ...], rebuild_all: bool) -> None:
    """Rebuild one or more container images.

    Running an image rebuild ensures the latest tool versions are
    persistently installed in the container. NAMES may be built-in images or
    user environments (``ai env list``), e.g. ``ai image rebuild pi,pi-python rust``.
    Without NAMES the configured default environment is rebuilt; with
    ``--all`` every image listed by ``ai image list`` is rebuilt.

    Requested images are rebuilt parents first; any other ``FROM aic:``
    parent is only built if it is missing.
    """
    if rebuild_all and names:
        raise click.UsageError("Pass either NAMES or --all, not both.")
    if rebuild_all:
        envs = list_environments()
    else:
        envs = [_resolve_env(ctx, name) for name in names or [None]]
    try:
        ensure_images(envs, dryrun=ctx.dryrun)
    except ValueError as exc:
        raise click.UsageError(str(exc)) from exc


@image.command("list")
def image_list() -> None:
    """List all images (built-in and user) with parent and built status."""
    names = list_environments()
    width = max((len(name) for name in names), default=0)
    for name in names:
        parent = parent_of(name)
        base = f"FROM aic:{parent}" if parent else "base image"
        built = "built" if image_exists(name) else "not built"
        stdout.print(f"{name:<{width}}  [{built:<9}]  ({base})")


@click.group("env")
def env() -> None:
    """Manage custom environments (customized images)."""


@env.command("list")
def env_list() -> None:
    """List available environments and whether their image is built."""
    for name in list_environments():
        built = "built" if image_exists(name) else "not built"
        stdout.print(f"{name}  [{built}]")


@env.command("new")
@click.argument("name", help="Name of the environment to create")
@click.option(
    "--from",
    "-f",
    "base",
    default=BASE_ENV,
    help="Image to inherit from (built-in or user image). [default: base]",
)
@click.option("--edit", "open_editor", is_flag=True, help="Open the new Containerfile in $EDITOR.")
def env_new(name: str, base: str, open_editor: bool) -> None:
    """Scaffold a new environment definition.

    Creates ``environments/<name>/Containerfile`` (extending ``aic:<base>``)
    under the user config directory. The base may be any built-in image
    (base, pi, claude, opencode, aichat, llm, full) or another user
    environment. Build it on first use or with ``ai image rebuild <name>``.
    """
    try:
        containerfile = create_environment(name, base=base)
    except ValueError as exc:
        raise click.UsageError(str(exc)) from exc
    stdout.print(f"Created environment '{name}' at {containerfile} (FROM aic:{base})")
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
def env_remove(ctx: Context, name: str, purge: bool) -> None:
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
