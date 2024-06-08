import os
import pytest
import datetime

from openai import OpenAI


@pytest.fixture
def api_key():
    yield os.environ.get("OPENAI_API_KEY")


@pytest.fixture
def client(api_key):
    yield OpenAI(api_key=api_key)


@pytest.mark.openai_api
def test_image_generation(client):
    prompt = "Generate a picture of a chat"
    model = "dall-e-3"
    response = client.images.generate(prompt=prompt, model=model)
    image_url = response.data[0].url
    created = datetime.datetime.fromtimestamp(response.created)
    pass


@pytest.mark.openai_api
def test_store_chat_session(client, test_db, model="gpt-4o"):
    msg = "Count to 10"
    response = client.chat.completions.create(
        model=model, messages=[{"role": "user", "content": msg}]
    )
    assistant_msg = response.choices[0].message
    role = assistant_msg.role
    content = assistant_msg.content
    print(response)


@pytest.mark.openai_api
def test_store_chat_session_with_context(client, test_db, model="gpt-4o"):
    msg = "Up to which number did you count before?"
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": "Count to 10"},
            {
                "role": "assistant",
                "content": "Sure, here you go: 1, 2, 3, 4, 5, 6, 7, 8, 9, 10",
            },
            {"role": "user", "content": msg},
        ],
    )
    assistant_msg = response.choices[0].message
    role = assistant_msg.role
    content = assistant_msg.content
    print(response)
