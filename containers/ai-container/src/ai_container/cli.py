import click
import subprocess
import importlib.resources
from pathlib import Path


def justfile():
    with importlib.resources.path("ai_container", "justfile") as path:
        return f"{path.resolve()}"


@click.group()
def ai():
    "AI command tools group."
    pass


@click.command("pi")
@click.argument("path")
@click.argument("args", nargs=-1)
def run_pi(path, args):
    "Run PI coding agent"
    path = f"{Path(path).resolve()}"
    subprocess.run(["just", "--justfile", justfile(), "pi", path, *args])


@click.command("opc")
@click.argument("path")
@click.argument("args", nargs=-1)
def run_opc(path, args):
    "Run OpenCode coding agent"
    path = f"{Path(path).resolve()}"
    subprocess.run(["just", "--justfile", justfile(), "opc", path, *args])


@click.command("aic")
@click.argument("path")
@click.argument("args", nargs=-1)
def run_aic(path, args):
    "Run aichat/aichat-command"
    path = f"{Path(path).resolve()}"
    subprocess.run(["just", "--justfile", justfile(), "aic", path, *args])


@click.command("llm")
@click.argument("path")
@click.argument("args", nargs=-1)
def run_llm(path, args):
    "Run llm/llm-command"
    path = f"{Path(path).resolve()}"
    subprocess.run(["just", "--justfile", justfile(), "llm", path, *args])


@click.command("shell")
@click.argument("path")
def shell(path):
    "Open a shell in the AI container"
    path = f"{Path(path).resolve()}"
    subprocess.run(["just", "--justfile", justfile(), "shell", path])


def _image(rebuild=False):
    """
    Make sure the image is avilable

    Args:
        rebuild: if true forces rebuild of the image even if it already exits

    """
    result = subprocess.run(["podman", "image", "exists", "aic"])
    if result.returncode != 0 or rebuild:
        subprocess.run(["just", "--justfile", justfile(), "build"])


# Overriding commands to include image existence check
def ensure_image(original_func):
    def wrapper(*args, **kwargs):
        _image(rebuild=False)
        return original_func(*args, **kwargs)

    return wrapper


ai.add_command(run_pi)
ai.add_command(run_opc)
ai.add_command(run_aic)
ai.add_command(run_llm)
ai.add_command(shell)
run_pi.callback = ensure_image(run_pi.callback)
run_opc.callback = ensure_image(run_opc.callback)
run_aic.callback = ensure_image(run_aic.callback)
run_llm.callback = ensure_image(run_llm.callback)
shell.callback = ensure_image(shell.callback)

if __name__ == "__main__":
    ai()
