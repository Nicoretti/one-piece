from dataclasses import asdict

import pytest

from konfy import Identifier, Konfy, Setting


@pytest.fixture()
def app():
    return "testapp"


@pytest.fixture()
def default_level():
    return "debug"


@pytest.fixture()
def env_level():
    return "error"


@pytest.fixture()
def default_timeout():
    return 45


@pytest.fixture()
def env_timeout():
    return 60


@pytest.fixture()
def defaults(default_level, default_timeout):
    return {"logging": {"level": default_level}, "timeout": default_timeout}


@pytest.fixture()
def env(env_level, env_timeout):
    return {"logging": {"level": env_level}, "timeout": env_timeout}


@pytest.fixture()
def konfy(app, defaults):
    return Konfy(
        application=app,
        cli=None,
        environment=None,
        app_config=None,
        user_config=None,
        system_config=None,
        defaults=defaults,
    )


@pytest.fixture()
def konfy_with_env_and_default(app, env, defaults):
    return Konfy(
        application=app,
        cli=None,
        environment=env,
        app_config=None,
        user_config=None,
        system_config=None,
        defaults=defaults,
    )


def test_konfy_configuration_with_defaults_only(konfy, defaults):
    expected = defaults
    actual = dict(konfy.config)
    assert actual == expected


def test_access_configuration_using_index_operator(konfy, default_level):
    cfg = konfy.config
    expected = default_level
    actual = cfg["logging"]["level"]
    assert actual == expected


def test_access_configuration_using_attribute_access(konfy, default_timeout):
    cfg = konfy.config
    expected = default_timeout
    actual = cfg.timeout
    assert actual == expected


def test_access_configuration_using_nested_attribute_access(konfy, default_level):
    cfg = konfy.config
    expected = default_level
    actual = cfg.logging.level
    assert actual == expected


def test_env_has_higher_priority_than_defaults(
    konfy_with_env_and_default,
    env_level,
    env_timeout,
):
    konfy = konfy_with_env_and_default
    cfg = konfy.config

    expected = env_level
    actual = cfg.logging.level

    assert actual == expected

    expected = env_timeout
    actual = cfg.timeout

    assert actual == expected


@pytest.mark.skip(reason="just a outline for the future")
def test_create_defaults():
    from konfy import Defaults, Konfy, Setting

    defaults = {"logging:level": "debug"}
    defaults = Defaults(
        [
            Setting(
                name="logging:level",
            ),
            Setting(
                ns="logging",
                name="facitlity",
                type=int,
                value=2,
                description="",
                help="",
            ),
        ],
    )

    settings = Konfy(
        name="foo",  # name of the application the konfy object is for
        cli={},  # Dict (parsed) / Could be argsparser (argparse object)
        environment=None,  # default os.environ
        app_config=None,  # default <cwd>app_name.toml
        user_config=None,  # default os sepecific e.g. linux = ~/config/app_name/config.toml
        system_config=None,  # default os specific e.g. linux /etc/<cwd>app_name.toml
        defaults=None,  # A iterable of default settings
    )
