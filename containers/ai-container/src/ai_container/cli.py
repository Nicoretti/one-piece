import subprocess
import importlib.resources
from pathlib import Path
from typing import Tuple, Callable, Any
import rich_click as click


def justfile() -> str:
    """Get the path to the justfile.
    
    Returns:
        str: Absolute path to the justfile.
    """
    with importlib.resources.path("ai_container", "justfile") as path:
        return f"{path.resolve()}"


@click.group()
def ai() -> None:
    """AI Container Command Tools.
    
    A unified interface for running various AI coding agents and tools
    within containers. Supports PI, OpenCode, aichat, and llm commands.
    """
    pass


@click.command("pi")
@click.argument("path")
@click.argument("args", nargs=-1)
def run_pi(path: str, args: Tuple[str, ...]) -> None:
    """Run PI coding agent.
    
    PI is a powerful coding agent that helps with code generation,
    analysis, and refactoring tasks within containers.
    
    Args:
        path: Directory or file path to work on.
        args: Additional arguments to pass to PI.
    """
    path = f"{Path(path).resolve()}"
    subprocess.run(["just", "--justfile", justfile(), "pi", path, *args])


@click.command("opc")
@click.argument("path")
@click.argument("args", nargs=-1)
def run_opc(path: str, args: Tuple[str, ...]) -> None:
    """Run OpenCode coding agent.
    
    OpenCode is an AI-powered coding assistant designed for
    enterprise development environments.
    
    Args:
        path: Directory or file path to work on.
        args: Additional arguments to pass to OpenCode.
    """
    path = f"{Path(path).resolve()}"
    subprocess.run(["just", "--justfile", justfile(), "opc", path, *args])


@click.command("aic")
@click.argument("path")
@click.argument("args", nargs=-1)
def run_aic(path: str, args: Tuple[str, ...]) -> None:
    """Run aichat/aichat-command.
    
    AIChat is an interactive AI chat interface for code assistance
    and general programming queries.
    
    Args:
        path: Directory or file path to work on.
        args: Additional arguments to pass to AIChat.
    """
    path = f"{Path(path).resolve()}"
    subprocess.run(["just", "--justfile", justfile(), "aic", path, *args])


@click.command("llm")
@click.argument("path")
@click.argument("args", nargs=-1)
def run_llm(path: str, args: Tuple[str, ...]) -> None:
    """Run llm/llm-command.
    
    LLM is a command-line tool for interacting with large language models
    and performing AI-powered text operations.
    
    Args:
        path: Directory or file path to work on.
        args: Additional arguments to pass to LLM.
    """
    path = f"{Path(path).resolve()}"
    subprocess.run(["just", "--justfile", justfile(), "llm", path, *args])


@click.command("shell")
@click.argument("path")
def shell(path: str) -> None:
    """Open a shell in the AI container.
    
    Launch an interactive shell session within the AI container
    for manual command execution and exploration.
    
    Args:
        path: Directory or file path to mount in the container.
    """
    path = f"{Path(path).resolve()}"
    subprocess.run(["just", "--justfile", justfile(), "shell", path])


def _image(rebuild: bool = False) -> None:
    """Ensure the container image is available.
    
    Args:
        rebuild: If True, forces rebuild of the image even if it already exists.
    """
    result = subprocess.run(["podman", "image", "exists", "aic"])
    if result.returncode != 0 or rebuild:
        subprocess.run(["just", "--justfile", justfile(), "build"])


# Overriding commands to include image existence check
def ensure_image(original_func: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator to ensure image exists before running a command.
    
    Args:
        original_func: The original callback function to wrap.
        
    Returns:
        Callable: A wrapper function that checks the image before execution.
    """
    def wrapper(*args: Any, **kwargs: Any) -> Any:
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
