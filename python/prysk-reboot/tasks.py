from invoke import Collection, task
from invokees.tasks import code, stderr, test  # noqa: E402


@task
def init(ctx):
    """Initializes the workspace, only should be run after initial checkout"""
    ctx.run("poetry install")
    stderr.print("[blue]Setting up Workspace[/blue]")
    stderr.print("[yellow]Installing pre-commit hooks[/yellow]")
    ctx.run("pre-commit install")


@task
def serve(ctx):
    """Build and serve documentation"""
    ctx.run('mkdocs serve')


docs = Collection('docs')
docs.add_task(serve)

ns = Collection(init, code, test, docs)
