from inspect import cleandoc
from atalk.storage import Image


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
