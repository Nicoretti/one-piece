import pytest
from aergia._model._storage import store
from aergia._db import initialize


@pytest.fixture
def test_db(tmp_path):
    name = "test"
    db = store(name, tmp_path)
    initialize(db)
    yield db
