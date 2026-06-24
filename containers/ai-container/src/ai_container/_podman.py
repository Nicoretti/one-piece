"""Podman setup helpers backed by the Podman Python SDK.

The actual interactive container launches still go through ``podman run -it``
(see :func:`run_container`) because attaching an interactive TTY is handled far
more reliably by the CLI than over the REST socket.
"""

from __future__ import annotations

import json
import importlib.resources
import logging
import shlex
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

IMAGE_NAME = "aic"
CONTAINERFILE = "Containerfile"
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


def image_exists() -> bool:
    """Return True if the ``aic`` image is present."""
    with podman_client() as client:
        return client.images.exists(IMAGE_NAME)


def build_image(*, dryrun: bool = False) -> None:
    """Build the ``aic`` image from the packaged Containerfile."""
    context = package_dir()
    if dryrun:
        _emit(
            [
                "podman", "build",
                "--tag", IMAGE_NAME,
                "--rm", "--pull",
                "--file", CONTAINERFILE,
                str(context),
            ]
        )
        return
    log.info("Building image '%s' from %s...", IMAGE_NAME, context)
    spinner = stderr.status(f"Building image '{IMAGE_NAME}'...", spinner="dots")
    with podman_client() as client, spinner:
        _, logs = client.images.build(
            path=str(context),
            dockerfile=CONTAINERFILE,
            tag=IMAGE_NAME,
            rm=True,
            pull=True,
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
    log.info("Image '%s' built.", IMAGE_NAME)


def ensure_volumes(*, dryrun: bool = False) -> None:
    """Create the persistence volumes that do not already exist."""
    with podman_client() as client:
        missing = (name for name in VOLUMES if not client.volumes.exists(name))
        for name in missing:
            if dryrun:
                _emit(["podman", "volume", "create", "--label", f"{VOLUME_LABEL}=", name])
            else:
                client.volumes.create(name=name, labels={VOLUME_LABEL: ""})


def ensure_image(*, rebuild: bool = False, dryrun: bool = False) -> None:
    """Ensure the image is available, building it when needed."""
    if rebuild or not image_exists():
        build_image(dryrun=dryrun)


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


def run_container(
        path: str,
        command: Sequence[str],
        *,
        include_pi_volume: bool = True,
        workdir_arg: bool = False,
        dryrun: bool = False,
) -> int:
    """Launch an interactive container.

    Args:
        path: Host directory to mount at ``/workspace``.
        command: Command (and args) to execute inside the container.
        include_pi_volume: Whether to mount the ``pi-config`` volume.
        workdir_arg: If True, append ``.`` after the command (used by opencode).
        dryrun: If True, print the ``podman run`` command instead of running it.

    Returns:
        The container process exit code.
    """
    specs = _volume_specs(path, include_pi_volume=include_pi_volume)
    volume_args = [arg for spec in specs for arg in ("--volume", spec)]
    trailing = ["."] if workdir_arg else []

    cmd = ["podman", "run", *volume_args, "-it", IMAGE_NAME, *command, *trailing]
    if dryrun:
        _emit(cmd)
        return 0
    return subprocess.run(cmd).returncode
