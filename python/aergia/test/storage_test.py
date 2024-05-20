import datetime

import pytest
from inspect import cleandoc
from aergia._storage import Image, store, initialize, TABLES, save, load


@pytest.fixture
def test_db(tmp_path):
    name = 'test'
    db = store(name, tmp_path)
    initialize(db, TABLES)
    yield db


def test_store_image(test_db):
    image = Image(
        id=None,
        name='Test.png',
        model='gpt-4o',
        prompt='Some test prompt',
        created=datetime.datetime.now(),
        blob=b'fake blob this is obviously no image data',
        openai_data=None
    )
    save(image, test_db)
    expected = 1
    actual = image.id
    assert expected == actual


def test_store_image_round_trip(test_db):
    image = Image(
        id=None,
        name='Test.png',
        model='gpt-4o',
        prompt='Some test prompt',
        created=datetime.datetime.now(),
        blob=b'fake blob this is obviously no image data',
        openai_data=None
    )
    save(image, test_db)

    expected = image
    actual = load(Image, image.name, test_db)
    assert expected == actual


def test_image_ddl():
    expected = cleandoc("""
    CREATE TABLE  IF NOT EXISTS images (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        blob BLOB NOT NULL
    );
    """)
    actual = Image.ddl
    assert expected == actual
