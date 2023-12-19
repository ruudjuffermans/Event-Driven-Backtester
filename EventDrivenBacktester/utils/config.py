import configparser


def get_config(name, config={}):
    config_parser = configparser.ConfigParser()
    config_parser.read("./config.ini")
    default_config = dict(config_parser["default"])
    default_config.update(config_parser[name])
    return {**default_config, **config}
