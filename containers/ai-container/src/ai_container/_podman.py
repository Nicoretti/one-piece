"""Podman setup helpers backed by the Podman Python SDK.

The actual interactive container launches still go through ``podman run -it``
(see :func:`run_container`) because attaching an interactive TTY is handled far
more reliably by the CLI than over the REST socket.
"""

from __future__ import annotations

import json
import importlib.resources
import logging
import os
import re
import shlex
import shutil
import subprocess
import sys
from inspect import cleandoc
from collections.abc import Iterator, Sequence
from contextlib import contextmanager
from pathlib import Path

from podman import PodmanClient
from podman.errors import APIError, PodmanError
from rich.console import Console

log = logging.getLogger(__name__)
stderr = Console(stderr=True)
stdout = Console()

IMAGE_REPO = "aic"
BASE_ENV = "base"
CONTAINERFILE = "Containerfile"
ENV_NAME_RE = re.compile(r"^[a-z0-9][a-z0-9_.-]*$")
ENV_TEMPLATE = cleandoc(
    """
    # {name} environment -- extends the ai-container base image.
    FROM {base}

    # Add your tooling below, e.g.:
    # RUN dnf install -y <packages>

    WORKDIR /workspace
    """
) + "\n"
VOLUME_LABEL = "aic"
WORKSPACE_MOUNT = "/workspace"
PI_VOLUME = "pi-config"

VOLUME_MOUNTS = {
    "state": "/root/.local/state",
    "share": "/root/.local/share",
    "config": "/root/.config",
    "claude": "/root/.claude",
    PI_VOLUME: "/root/.pi",

}
ANONYMOUS_VOLUME_OVERLAYS = ["/root/.config/nvim"]

VOLUMES = tuple(VOLUME_MOUNTS)

SERVICE_HINT = (
        cleandoc(
            """
        Could not reach the Podman service.
        Start it with:
          systemctl --user enable --now podman.socket
        or run it directly:
          podman system service --time=0
    
        Underlying error: {error}
        """
        )
        + "\n"
)


def _emit(cmd: Sequence[str]) -> None:
    """Print a podman command instead of executing it (dry run)."""
    stdout.print(shlex.join(cmd), soft_wrap=True, highlight=False)


def package_dir() -> Path:
    """Return the directory that holds the packaged Containerfile."""
    with importlib.resources.path("ai_container", CONTAINERFILE) as path:
        return path.resolve().parent


def image_tag(env: str) -> str:
    """Return the image tag for an environment (e.g. ``rust`` -> ``aic:rust``)."""
    return f"{IMAGE_REPO}:{env}"


def config_dir() -> Path:
    """Return the user config directory for ai-container (honors XDG)."""
    base = os.environ.get("XDG_CONFIG_HOME") or (Path.home() / ".config")
    return Path(base) / "ai-container"


def environments_dir() -> Path:
    """Return the directory that holds user-defined environment definitions."""
    return config_dir() / "environments"


def environment_context(env: str) -> Path:
    """Return the build-context directory for an environment definition."""
    return environments_dir() / env


def environment_exists(env: str) -> bool:
    """Return True if a definition exists for ``env`` (``base`` always does)."""
    if env == BASE_ENV:
        return True
    return (environment_context(env) / CONTAINERFILE).is_file()


def list_environments() -> list[str]:
    """Return all known environments: ``base`` plus discovered definitions."""
    root = environments_dir()
    discovered = (
        path.name
        for path in sorted(root.iterdir())
        if path.is_dir() and (path / CONTAINERFILE).is_file()
    ) if root.is_dir() else ()
    return [BASE_ENV, *discovered]


@contextmanager
def podman_client() -> Iterator[PodmanClient]:
    """Yield a connected :class:`PodmanClient`.

    Uses the default Podman service socket resolution (active
    ``podman system connection`` or the rootless socket under
    ``$XDG_RUNTIME_DIR``). Emits a friendly hint if the service is not
    reachable.
    """
    client = PodmanClient()
    try:
        if not client.ping():
            raise PodmanError("Podman service did not respond to ping.")
        yield client
    except (APIError, PodmanError, FileNotFoundError, ConnectionError) as exc:
        log.error(SERVICE_HINT.format(error=exc))
        client.close()
        sys.exit(1)
    finally:
        client.close()


def image_exists(env: str = BASE_ENV) -> bool:
    """Return True if the image for ``env`` is present."""
    with podman_client() as client:
        return client.images.exists(image_tag(env))


def build_image(env: str = BASE_ENV, *, dryrun: bool = False) -> None:
    """Build the image for ``env``.

    The ``base`` environment is built from the packaged Containerfile; other
    environments are built from ``environments/<env>/Containerfile`` and are
    expected to start ``FROM aic:base``.
    """
    if env == BASE_ENV:
        context = package_dir()
        pull = True
    else:
        context = environment_context(env)
        pull = False
    tag = image_tag(env)
    if dryrun:
        _emit(
            [
                "podman", "build",
                "--tag", tag,
                "--rm", *(["--pull"] if pull else []),
                "--file", CONTAINERFILE,
                str(context),
            ]
        )
        return
    log.info("Building image '%s' from %s...", tag, context)
    spinner = stderr.status(f"Building image '{tag}'...", spinner="dots")
    with podman_client() as client, spinner:
        _, logs = client.images.build(
            path=str(context),
            dockerfile=CONTAINERFILE,
            tag=tag,
            rm=True,
            pull=pull,
        )
        logs = (log.decode() for log in logs)
        logs = (json.loads(log) for log in logs)
        for chunk in logs:
            if stream := chunk.get("stream"):
                if line := stream.strip():
                    log.info(line)
            if error := chunk.get("error"):
                log.error(error)
                sys.exit(1)
    log.info("Image '%s' built.", tag)


def ensure_volumes(*, dryrun: bool = False) -> None:
    """Create the persistence volumes that do not already exist."""
    with podman_client() as client:
        missing = (name for name in VOLUMES if not client.volumes.exists(name))
        for name in missing:
            if dryrun:
                _emit(["podman", "volume", "create", "--label", f"{VOLUME_LABEL}=", name])
            else:
                client.volumes.create(name=name, labels={VOLUME_LABEL: ""})


def ensure_image(env: str = BASE_ENV, *, rebuild: bool = False, dryrun: bool = False) -> None:
    """Ensure the image for ``env`` is available, building it when needed.

    For non-base environments the base image is ensured first, since the
    environment layer is built ``FROM aic:base``.
    """
    if env != BASE_ENV:
        ensure_image(BASE_ENV, dryrun=dryrun)
    if rebuild or dryrun or not image_exists(env):
        build_image(env, dryrun=dryrun)


def _volume_specs(path: str, *, include_pi_volume: bool) -> list[str]:
    """Return ``name:target`` volume specs for a container run.

    Selection (which volumes to mount) is kept separate from the host
    workspace bind mount.
    """
    host_path = str(Path(path).resolve())
    named = (
        f"{name}:{target}"
        for name, target in VOLUME_MOUNTS.items()
        if include_pi_volume or name != PI_VOLUME
    )
    return [f"{host_path}:{WORKSPACE_MOUNT}:rw,z", *named, *ANONYMOUS_VOLUME_OVERLAYS]


def valid_env_name(env: str) -> bool:
    """Return True if ``env`` is a usable environment / image-tag name."""
    return bool(ENV_NAME_RE.match(env))


def create_environment(env: str) -> Path:
    """Scaffold a new environment definition and return its Containerfile path.

    Raises:
        ValueError: If the name is invalid or the definition already exists.
    """
    if not valid_env_name(env):
        raise ValueError(
            f"Invalid environment name '{env}'. Use lowercase letters, digits, "
            "'.', '_' or '-' (must start with a letter or digit)."
        )
    if env == BASE_ENV:
        raise ValueError("'base' is reserved; rebuild it with 'ai image rebuild'.")
    containerfile = environment_context(env) / CONTAINERFILE
    if containerfile.exists():
        raise ValueError(f"Environment '{env}' already exists at {containerfile}.")
    containerfile.parent.mkdir(parents=True, exist_ok=True)
    containerfile.write_text(ENV_TEMPLATE.format(name=env, base=image_tag(BASE_ENV)))
    return containerfile


def remove_environment(env: str, *, purge: bool = False, dryrun: bool = False) -> None:
    """Delete an environment definition; optionally remove its image too.

    Raises:
        ValueError: If the environment does not exist or is ``base``.
    """
    if env == BASE_ENV:
        raise ValueError("The 'base' environment cannot be removed.")
    context = environment_context(env)
    if not (context / CONTAINERFILE).is_file():
        raise ValueError(f"Unknown environment '{env}'.")
    if dryrun:
        _emit(["rm", "-rf", str(context)])
        if purge:
            _emit(["podman", "rmi", image_tag(env)])
        return
    shutil.rmtree(context)
    if purge:
        with podman_client() as client:
            if client.images.exists(image_tag(env)):
                client.images.remove(image_tag(env), force=True)


def run_container(
        path: str,
        command: Sequence[str],
        *,
        env: str = BASE_ENV,
        include_pi_volume: bool = True,
        workdir_arg: bool = False,
        dryrun: bool = False,
) -> int:
    """Launch an interactive container.

    Args:
        path: Host directory to mount at ``/workspace``.
        command: Command (and args) to execute inside the container.
        env: Environment whose image (``aic:<env>``) to run.
        include_pi_volume: Whether to mount the ``pi-config`` volume.
        workdir_arg: If True, append ``.`` after the command (used by opencode).
        dryrun: If True, print the ``podman run`` command instead of running it.

    Returns:
        The container process exit code.
    """
    specs = _volume_specs(path, include_pi_volume=include_pi_volume)
    volume_args = [arg for spec in specs for arg in ("--volume", spec)]
    trailing = ["."] if workdir_arg else []

    cmd = ["podman", "run", *volume_args, "-it", image_tag(env), *command, *trailing]
    if dryrun:
        _emit(cmd)
        return 0
    return subprocess.run(cmd).returncode
