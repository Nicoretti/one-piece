import datetime

from aergia._model._storage import save, load
from aergia._model._data import Image


def test_store_image(test_db):
    image = Image(
        id=None,
        name='Test.png',
        model='gpt-4o',
        prompt='Some test prompt',
        revised_prompt='revised: Some test prompt',
        created=datetime.datetime.now(),
        blob=b'fake blob this is obviously no image data',
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
        revised_prompt='revised: Some test prompt',
        created=datetime.datetime.now(),
        blob=b'fake blob this is obviously no image data',
    )
    save(image, test_db)

    expected = image
    actual = load(Image, image.name, test_db)
    assert expected == actual
