import pytest
from aergia._config._settings import Setting
from aergia._config._env import env, from_env, env_key


@pytest.mark.parametrize("setting,expected", [
    (Setting(
        name="model",
        type=str,
        default="gpt-4o",
        description="Model to use"
    ),
     ("MODEL", "gpt-4o")
    ),
    (Setting(
        name="model",
        type=str,
        prefix="chat",
        default="gpt-4o",
        description="Model to use"
    ),
     ("CHAT_MODEL", "gpt-4o")
    ),
    (Setting(
        name="model",
        type=str,
        prefix="aergia_chat",
        default="gpt-4o",
        description="Model to use"
    ),
     ("AERGIA_CHAT_MODEL", "gpt-4o")
    ),
    (Setting(
        name="model",
        type=str,
        prefix="aergia-chat",
        default="gpt-4o",
        description="Model to use"
    ),
     ("AERGIA_CHAT_MODEL", "gpt-4o")
    ),
])
def test_setting_to_env(setting, expected):
    actual = env(setting)
    assert actual == expected


@pytest.mark.parametrize("setting,env,expected", [
    (
            Setting(
                name="limit",
                type=int,
                default=5,
                description="Fetch limit"
            ),
            {"LIMIT": "2", "A": "B"},
            2
    ),
    (
            Setting(
                name="timeout",
                type=float,
                default=3.0,
                description="timeout for network connections"
            ),
            {"TIMEOUT": "2.0", "A": "B"},
            2.0
    ),
    (
            Setting(
                name="model",
                type=str,
                default="gpt-4o",
                description="Model to use"
            ),
            {"MODEL": "gpt-4", "A": "B"},
            "gpt-4"
    ),
    (
            Setting(
                name="stream",
                type=bool,
                default="on",
                description="Enable streaming"
            ),
            {"STREAM": "TRUE", "A": "B"},
            True
    ),
])
def test_setting_from_env(setting, env, expected):
    actual = from_env(
        name=env_key(setting),
        type=setting.type,
        env=env
    )
    assert actual == expected


def test_setting_in_namespace_to_env():
    pass


#def test_iterate_trough_settings():
#    for s in settings:
#        pass
#
#
#def test_build_settings():
#    ns = Namespace(settings, ns)
#    for s in settings:
#        pass
#
#
#def test_access_settings():
#    namespaces = []
#    settings = []
#    aergia_ns = Namespace(name="aergia", settings, namespaces)
#
#    aergia = Settings(aergia_ns)
#
#    aergia.update(cli={}, env={}, config={})
#
#    # only default value is defined
#    aergia.debug
#
#    # default is overwritten by cli
#    aergia.update(cli={"--debug"})
#    aergia.debug
#
#    # default is overwritten by envv
#    aergia.update(env={"DEBUG": "YES"})
#    aergia.debug
#
#    aergia.update_from_cli()
#    aergia.defaults()
#
#    aeargia.stream
#    for s in settings:
#        pass
