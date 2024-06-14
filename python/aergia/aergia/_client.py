from openai import OpenAI, AsyncClient
from enum import Enum, auto


class Type(Enum):
    Async = auto()
    Sync = auto()


def _select_client(backend, client_type):
    OPENAI = {Type.Async: AsyncClient, Type.Sync: OpenAI}
    backends = {"openai": OPENAI}

    try:
        selected_backend = backends[backend]
    except KeyError as ex:
        err_msg = f"Backend ({backend}) is not supported."
        raise Exception(err_msg) from ex

    try:
        klass = selected_backend[client_type]
    except KeyError as ex:
        err_msg = f"Streaming is not supported by {selected_backend}."
        raise Exception(err_msg) from ex

    return klass


def build_client(backend, api_key, base_url=None, client_type=Type.Sync):
    if base_url is None:
        base_url = "https://api.openai.com/v1"
    Client = _select_client(backend, client_type)
    return Client(base_url=base_url, api_key=api_key)
