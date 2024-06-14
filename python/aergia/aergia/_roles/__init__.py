import json

import jinja2.exceptions
from jinja2 import FileSystemLoader, ChoiceLoader, PackageLoader, Environment


class RoleNotFound(Exception):
    pass


def parse(role_spec):
    def is_kwarg(arg):
        return "=" in arg

    parts = role_spec.split(":")
    role = parts.pop(0)
    args = [arg for arg in parts if not is_kwarg(arg)]
    kwargs = {
        k: v for k, v in
        [tuple(kwarg.split("=")) for kwarg in parts if is_kwarg(kwarg)]
    }
    return role, args, kwargs


def execute(role_spec, input=None, role_paths=None):
    role_paths = role_paths or []
    role_paths = role_paths if not isinstance(role_spec, str) else list(role_paths)
    role, args, kwargs = parse(role_spec)
    template, _metadata = load(role, role_paths)
    # TODO: Add parameter check etc. based on metadata etc.
    prompt = render(template, args, kwargs, input)
    return prompt


def load(role, paths=None):
    paths = paths or []
    builtin_roles = PackageLoader(package_name='aergia', package_path='_roles')
    custom_roles = FileSystemLoader(list(paths))
    loader = ChoiceLoader([
        builtin_roles,
        custom_roles
    ])
    env = Environment(loader=loader)
    try:
        template = env.get_template(f"{role}.role")
    except jinja2.exceptions.TemplateNotFound as ex:
        raise RoleNotFound(f"Role [{role}] not found, details: File {ex} not found.") from ex

    try:
        metadata = env.get_template(f"{role}.role.meta")
        metadata = json.loads(metadata.render())
    except jinja2.exceptions.TemplateNotFound:
        metadata = {}

    return template, metadata


def render(template, args, kwargs, input):
    role_arguments = {
        'args': args, 'kwargs': kwargs, 'input': input
    }
    return template.render(role=role_arguments)

# TODO:
# Consider adding a role metadata feature that can be used for validation if desired, and for
# built-in roles by default ... metadata is also a model that should be executed with ...
# Also, validation of metadata spec could be done using JSON schemas.
