from shutil import which

from invoke import task

from invokees.tasks import command


@task(aliases=("init",))
def initialize(context, color=True):
    """
    Initialize configurations

    Args:
        context: invoke context.
        color: whether to use colors (default: True).
    """

    def _install_pre_commit(ctx):
        pre_commit = ["pre-commit", "install", "-t", "pre-commit", "-t", "pre-push"]
        ctx.run(command(*pre_commit), pty=color)

    def _install_github_cli(ctx):
        if not which("gh"):
            ctx.run("sudo dnf install gh", pty=color)

    _install_pre_commit(context)
    _install_github_cli(context)
