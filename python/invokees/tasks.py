import sys
from pathlib import Path

from invoke import Collection

PROJECT_ROOT = Path(__file__)
sys.path.append(f"{PROJECT_ROOT.parent / 'src'}")

from invokees.tasks import (  # noqa: E402
    code,
    docs,
    release,
    self,
    test,
)

ns = Collection(code, test, self, release, docs)
