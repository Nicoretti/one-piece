from invoke import Collection
from dukh import (
    packages,
    ssh,
    tls,
)

ns = Collection(packages.ns, ssh.ns, tls.ns)
