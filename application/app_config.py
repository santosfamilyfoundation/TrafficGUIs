# app_config.py
from ConfigParser import SafeConfigParser


class AppConfig(object):
    PROJECT_DIR = None
    TI_INSTALL_DIR = None

    def __init__(self):
        super(AppConfig, self).__init__()

    @classmethod
    def load_application_config(cls):
        config_parser = SafeConfigParser()
        config_parser.read(".application")
        cls.PROJECT_DIR = config_parser.get("info", "default_project_dir")
        cls.TI_INSTALL_DIR = config_parser.get("info", "ti_install_dir")

    # TODO: class method for writing to application config file
