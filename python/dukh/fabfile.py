from invoke import Collection
from dukh import (
    packages,
    ssh,
    tls,
    exasol,
    errno,
    shell
)

ns = Collection(packages.ns, ssh.ns, tls.ns, exasol.ns, errno.ns, shell.ns)
