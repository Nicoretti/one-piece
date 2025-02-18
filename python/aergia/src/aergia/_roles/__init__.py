import json
from pathlib import Path
from typing import Any, Dict, List, Tuple

from jinja2 import ChoiceLoader, Environment, FileSystemLoader, PackageLoader, Template
from jinja2.exceptions import TemplateNotFound


class RoleNotFound(Exception):
    """
    Exception indicating that the specified role could not be found.
    """


def parse(role_spec: str) -> Tuple[str, List[str], Dict[str, Any]]:
    """
    Parse the role specification string.

    Args:
        role_spec: Role spec string.

    Returns:
        tuple: Contains role, list of arguments and dictionary of keyword arguments.
    """

    def is_kwarg(arg):
        return "=" in arg

    parts = role_spec.split(":")
    role = parts.pop(0)
    args = [arg for arg in parts if not is_kwarg(arg)]
    kwargs = {k: v for k, v in [tuple(kwarg.split("=")) for kwarg in parts if is_kwarg(kwarg)]}
    return role, args, kwargs


def prompt(role_spec: str, input: str = None, role_paths: str | List = None) -> Tuple[str, str]:
    """
    Create a prompt based on given role spec and input.

    Args:
        role_spec: Role spec which shall be used for creating the prompt.
        input: User input which will be provided to the role.
        role_paths: List of custom paths to search for roles on the file system.

    Returns:
        The prompt and the model which should be used for executing the role.
    """
    role_paths = role_paths or []
    role_paths = role_paths if not isinstance(role_spec, str) else list(role_paths)
    role, args, kwargs = parse(role_spec)
    template, metadata = load(role, role_paths)
    # TODO: Add parameter check etc. based on metadata etc.
    role_prompt = render(template, args, kwargs, input)
    model = metadata.get("model", None)
    return role_prompt, model


def create_env(paths: List | None = None) -> Environment:
    """
    Create an environment for finding role templates and metadata.

    Args:
        paths: A list of custom paths to search for roles on the filesystem.

    Returns:
        Jinja environment which provides access to the roles.
    """
    paths = paths or []
    builtin_roles = PackageLoader(package_name="aergia", package_path="_roles")
    custom_roles = FileSystemLoader(list(paths))
    loader = ChoiceLoader([builtin_roles, custom_roles])
    return Environment(loader=loader)


def load(role: str, paths: List[str | Path] | None = None) -> Tuple[Template, Dict[str, Any]]:
    """
    Load role template and role metadata.

    Args:
        role: Name of the role which shall be loaded.
        paths: A list of custom paths to search for roles on the filesystem.

    Raises:
        RoleNotFound: If role template not found in any of the paths.

    Returns:
        Role template and role metadata.
    """
    env = create_env(paths)
    try:
        template = env.get_template(f"{role}.role")
    except TemplateNotFound as ex:
        msg = f"Role {role} could not be found, details: {ex}"
        raise RoleNotFound(msg) from ex
    try:
        metadata = env.get_template(f"{role}.role.meta")
        metadata = json.loads(metadata.render())
    except TemplateNotFound:
        metadata = {}

    return template, metadata


def render(
    template: Template,
    args: List[Any] | None,
    kwargs: Dict[str, Any] | None,
    input: str | None,
) -> str:
    """
    Render a specific role template using the given the args, kwargs and input.

    Args:
        template: Role tempalte which will be used.
        args: List of positional argument values.
        kwargs: Dictionary of keyword arguments.
        input: User input provided to the role.

    Returns:
        Final role prompt rendered as from the template string.
    """
    args = args or list()
    kwargs = kwargs or dict()
    role_arguments = {"args": args, "kwargs": kwargs, "input": input}
    return template.render(role=role_arguments)
