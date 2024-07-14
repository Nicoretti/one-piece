from invoke import Context, task, Collection
from enum import Enum


class Types(Enum):
    ed = "e"
    ba = "b"


@task
def generate_ssh_key(ctx: Context, type: Types = Types.ed, comment=None):
    """Generate an SSH-Keypair

    Args:
        context: invoke context.
        type: to search for python files (default: '.').
        comment: issues instead of reporting them (default: None).
    """
    if comment is None:
        input("foo: ")
        return
    ctx.run(f'ssh-keygen -t {type} -C "{comment}"')


ns = Collection("ssh")
ns.add_task(generate_ssh_key, name="generate-key")
