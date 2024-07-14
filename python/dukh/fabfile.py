from invoke import Collection
from dukh import (
    packages,
    ssh,
)

ns = Collection(packages.ns, ssh.ns)
