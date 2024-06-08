import pytest
from aergia._model._storage import store, initialize


@pytest.fixture
def test_db(tmp_path):
    name = 'test'
    db = store(name, tmp_path)
    initialize(db)
    yield db
