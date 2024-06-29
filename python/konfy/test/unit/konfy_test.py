from konfy import Konfy

def test_create_Konfy_object():

    konfy = Konfy(
        application,  # name of the application the konfy object is for
        cli=None,  # Dict (parsed) / Could be argsparser (argparse object)
        environment=None,  # default os.environ
        app_config=None,  # default <cwd>app_name.toml
        user_config=None,  # default os sepecific e.g. linux = ~/config/app_name/config.toml
        system_config=None,  # default os specific e.g. linux /etc/<cwd>app_name.toml
        defaults=None,  # A dictironary containg the defautls for settings
    )

    cfg = konfy.config
    level = cfg.logging.level
    facitlity = cfg['logging']['facitlity']


def test_create_defaults():
    from konfy import Konfy, Defaults, Setting

    defaults = { "logging:level": "debug" }
    defaults = Defaults([
        Setting(
            name="logging:level", 

        ),
        Setting(
            ns="logging",
            name="facitlity", 
            type=int,
            value=2,
            description="",
            help=""
        ),

        ])



    settings = Konfy(
        name="foo",  # name of the application the konfy object is for
        cli={},  # Dict (parsed) / Could be argsparser (argparse object)
        environment=None,  # default os.environ
        app_config=None,  # default <cwd>app_name.toml
        user_config=None,  # default os sepecific e.g. linux = ~/config/app_name/config.toml
        system_config=None,  # default os specific e.g. linux /etc/<cwd>app_name.toml
        defaults=None,  # A iterable of default settings
    )
