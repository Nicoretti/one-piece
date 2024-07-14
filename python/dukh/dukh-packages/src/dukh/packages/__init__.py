from dataclasses import dataclass
from typing import Iterable
from invoke import Context, task, Collection


@dataclass(frozen=True)
class PackageManager:
    ctx: Context

    def update_all_packages(self):
        self.ctx.sudo("apt update", pty=True)
        self.ctx.sudo("apt upgrade", pty=True)


# package.name => package manager name
APT = {"fish-shell": "fish", "docker": "docker.io"}


@dataclass(frozen=True)
class Package:
    id: int
    name: str
    description: str


def all_packages() -> Iterable[Package]:
    return {
        Package(
            id=1,
            name="fish-shell",
            description="A shell geared towards interactive use",
        ),
        Package(id=2, name="nvim", description="Neo-VIM Editor"),
        Package(id=3, name="starship", description="Cross Shell Prompt"),
        Package(id=4, name="starship", description="Cross Shell Prompt"),
        Package(id=5, name="zellij", description="Cross Shell Prompt"),
    }


default_packages = {
    "fish-shell",
    "starship",  # manual install & updaet
    "zellij",  # manual install & update
    "nvim",  # manual install & update
}

dms = {
    "docker",
}


@task
def list_packages(c):
    """List all available packages"""
    for package in all_packages():
        print(package)


@task
def update_packages(c):
    """Update the system packages (only apt is supported yet)"""
    pkg_mgr = PackageManager(ctx=c)
    pkg_mgr.update_all_packages()


ns = Collection("pkg")
ns.add_task(list_packages, name="list")
ns.add_task(update_packages, name="update")
