"""Podman setup helpers backed by the Podman Python SDK.

The actual interactive container launches still go through ``podman run -it``
(see :func:`run_container`) because attaching an interactive TTY is handled far
more reliably by the CLI than over the REST socket.
"""
from __future__ import annotations

import importlib.resources
import subprocess
import sys
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator, Sequence

import rich_click as click
from podman import PodmanClient
from podman.errors import APIError, PodmanError

IMAGE_NAME = "aic"
CONTAINERFILE = "Containerfile"

# Named volumes that persist tool configuration/state across runs.
VOLUMES = ("state", "share", "config", "pi-config")

# Where each named volume is mounted inside the container.
VOLUME_MOUNTS = {
    "state": "/root/.local/state",
    "share": "/root/.local/share",
    "config": "/root/.config",
    "pi-config": "/root/.pi",
}


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
        click.secho(
            "Could not reach the Podman service.\n"
            "Start it with:\n"
            "  systemctl --user enable --now podman.socket\n"
            "or run it directly:\n"
            "  podman system service --time=0\n"
            f"\nUnderlying error: {exc}",
            fg="red",
            err=True,
        )
        client.close()
        sys.exit(1)
    finally:
        client.close()


def image_exists() -> bool:
    """Return True if the ``aic`` image is present."""
    with podman_client() as client:
        return client.images.exists(IMAGE_NAME)


def build_image() -> None:
    """Build the ``aic`` image from the packaged Containerfile."""
    context = package_dir()
    click.secho(f"Building image '{IMAGE_NAME}' from {context}...", fg="cyan")
    with podman_client() as client:
        _, logs = client.images.build(
            path=str(context),
            dockerfile=CONTAINERFILE,
            tag=IMAGE_NAME,
            rm=True,
            pull=True,
        )
        for chunk in logs:
            stream = chunk.get("stream") if isinstance(chunk, dict) else None
            if stream:
                click.echo(stream, nl=False)
            error = chunk.get("error") if isinstance(chunk, dict) else None
            if error:
                click.secho(error, fg="red", err=True)
                sys.exit(1)
    click.secho(f"Image '{IMAGE_NAME}' built.", fg="green")


def ensure_volumes() -> None:
    """Create the persistence volumes if they do not already exist."""
    with podman_client() as client:
        for name in VOLUMES:
            if not client.volumes.exists(name):
                client.volumes.create(name=name, labels={"aic": ""})


def ensure_image(rebuild: bool = False) -> None:
    """Ensure the image is available, building it when needed."""
    if rebuild or not image_exists():
        build_image()


def _volume_args() -> list[str]:
    """Build the ``--volume`` arguments for the named persistence volumes."""
    args: list[str] = []
    for name, target in VOLUME_MOUNTS.items():
        args += ["--volume", f"{name}:{target}"]
    return args


def run_container(
    path: str,
    command: Sequence[str],
    *,
    include_pi_volume: bool = True,
    workdir_arg: bool = False,
) -> int:
    """Launch an interactive container.

    Args:
        path: Host directory to mount at ``/workspace``.
        command: Command (and args) to execute inside the container.
        include_pi_volume: Whether to mount the ``pi-config`` volume.
        workdir_arg: If True, append ``.`` after the command (used by opencode).

    Returns:
        The container process exit code.
    """
    host_path = str(Path(path).resolve())

    volume_args: list[str] = ["--volume", f"{host_path}:/workspace:rw,z"]
    for name, target in VOLUME_MOUNTS.items():
        if name == "pi-config" and not include_pi_volume:
            continue
        volume_args += ["--volume", f"{name}:{target}"]

    cmd = ["podman", "run", *volume_args, "-it", IMAGE_NAME, *command]
    if workdir_arg:
        cmd.append(".")

    return subprocess.run(cmd).returncode
