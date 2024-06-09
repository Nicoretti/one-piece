import datetime

from aergia._model._load import load
from aergia._model._save import save
from aergia._model._data import Image, Session, Message


def test_store_image(test_db):
    image = Image(
        id=None,
        name="Test.png",
        model="gpt-4o",
        prompt="Some test prompt",
        revised_prompt="revised: Some test prompt",
        created=datetime.datetime.now(),
        blob=b"fake blob this is obviously no image data",
    )
    save(image, test_db)
    expected = 1
    actual = image.id
    assert expected == actual


def test_store_image_round_trip(test_db):
    image = Image(
        id=None,
        name="Test.png",
        model="gpt-4o",
        prompt="Some test prompt",
        revised_prompt="revised: Some test prompt",
        created=datetime.datetime.now(),
        blob=b"fake blob this is obviously no image data",
    )
    save(image, test_db)

    expected = image
    actual = load(Image, key="name", value=image.name, db=test_db)
    assert expected == actual


def test_store_new_session(test_db):
    session = Session(
        id=None,
        name="test-session",
        model="gpt-4o",
        created=datetime.datetime.now(),
        temperature=1.0,
    )
    save(session, test_db)
    expected = 1
    actual = session.id
    assert expected == actual


def test_load_session(test_db):
    session = Session(
        id=None,
        name="test-session",
        model="gpt-4o",
        created=datetime.datetime.now(),
        temperature=1.0,
    )
    save(session, test_db)

    expected = session
    actual = load(Session, key="id", value=1, db=test_db)

    assert expected == actual


def test_store_new_message(test_db):
    message = Message(
        id=None,
        content="some content message",
        model="gpt-4o",
        role="user",
        created=datetime.datetime.now(),
        session_id=None,
    )
    save(message, test_db)
    expected = 1
    actual = message.id
    assert expected == actual


def test_load_message(test_db):
    message = Message(
        id=None,
        content="some content message",
        model="gpt-4o",
        role="user",
        created=datetime.datetime.now(),
        session_id=None,
    )
    save(message, test_db)

    expected = [message]
    actual = list(load(Message, key="id", value=1, db=test_db))

    assert expected == actual


def test_load_all_messages_of_session(test_db):
    session_id = 2
    messages = [
        Message(
            id=None,
            content="some content message1",
            model="gpt-4o",
            role="user",
            created=datetime.datetime.now(),
            session_id=session_id,
        ),
        Message(
            id=None,
            content="this is a reply of reply",
            model="gpt-4o",
            role="assistant",
            created=datetime.datetime.now(),
            session_id=session_id,
        ),
    ]
    for m in messages:
        save(m, test_db)

    expected = messages
    actual = list(load(Message, key="session_id", value=session_id, db=test_db))

    assert expected == actual
