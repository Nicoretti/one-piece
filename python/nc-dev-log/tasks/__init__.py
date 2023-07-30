from invoke import Collection
from invokees.tasks import code, test

from tasks import bucketfs, environment, errno, tls

namespace = Collection(errno, tls, bucketfs, environment, code, test)
