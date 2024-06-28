import pytest
from inspect import cleandoc

from aergia._config._toml import from_toml


@pytest.fixture
def config():
    cfg = cleandoc(
        """
        backend = "openai" # default backend
    
        [openai]
        base-url = "https://api.openai.com/v1"
        api-key = "123123foo" 
        log = "error"
        client-type = "async"
        """
    )
    yield cfg


@pytest.fixture
def toml(tmp_path, config):
    name = "aergia.toml"
    file = tmp_path / name
    file.write_text(config)
    yield file


def test_load_default_config(toml):
    expected = {
        "backend": "openai",
        "openai": {
            "log": "error",
            "api-key": "123123foo",
            "base-url": "https://api.openai.com/v1",
        },
    }
    actual = from_toml(toml)
    assert actual == expected
