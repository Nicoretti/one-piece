import os
import pytest
import datetime

from openai import OpenAI


@pytest.fixture
def api_key():
    yield os.environ.get("OPENAI_API_KEY")


@pytest.fixture
def client(api_key):
    yield OpenAI(
        api_key=api_key
    )


@pytest.mark.openai_api
def test_image_generation(client):
    prompt = "Generate a picture of a chat"
    model = "dall-e-3"
    response = client.images.generate(prompt=prompt, model=model)
    image_url = response.data[0].url
    created = datetime.datetime.fromtimestamp(response.created)
    pass

