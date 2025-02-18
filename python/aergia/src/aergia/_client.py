from enum import Enum, auto

from openai import AsyncClient, AzureOpenAI, OpenAI


class Type(Enum):
    Async = auto()
    Sync = auto()


def _select_client(backend, client_type):
    OPENAI = {Type.Async: AsyncClient, Type.Sync: OpenAI}
    AZURE = {Type.Sync: AzureOpenAI}
    backends = {"openai": OPENAI, "azure": AZURE}

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


def _kwargs(backend, settings):
    kwargs = {"api_key": settings["api-key"]}
    klass = _select_client(backend, Type.Sync)
    if issubclass(klass, AzureOpenAI):
        kwargs["api_version"] = settings.get("api-version", "2024-02-01")
        kwargs["azure_endpoint"] = settings["base-url"]
    else:
        kwargs["base_url"] = settings["base-url"]
    return kwargs


def build_client(backend, settings):
    Client = _select_client(backend, Type.Sync)
    kwargs = _kwargs(backend, settings)
    return Client(**kwargs)
