import os
import pytest
import datetime
from aergia._client import build_client, Type
from aergia._cli._command._utilities import TextBuffer

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


@pytest.mark.openai_api
def test_store_chat_session(client, test_db, model="gpt-4o"):
    msg = "Count to 10"
    response = client.chat.completions.create(
        model=model, messages=[{"role": "user", "content": msg}]
    )
    assistant_msg = response.choices[0].message
    role = assistant_msg.role
    content = assistant_msg.content


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
        stream=True,
    )
    for b in response:
        print(b)
    assistant_msg = response.choices[0].message
    role = assistant_msg.role
    content = assistant_msg.content


@pytest.mark.openai_api
@pytest.mark.anyio
async def test_async_chat(api_key):
    def is_chunk_valid(chunk):
        return chunk.choices is not None and len(chunk.choices) > 0

    client = build_client(backend="openai", api_key=api_key, client_type=Type.Async)
    result = await client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": "count to 10"}],
        stream=True,
    )
    with TextBuffer() as buffer:
        stream = (c async for c in result if is_chunk_valid(c))
        async for chunk in stream:
            text = chunk.choices[0].delta.content or ""
            model = chunk.model
            buffer.append(text)

    assert model.startswith("gpt-4o")
    assert "" == buffer.content
