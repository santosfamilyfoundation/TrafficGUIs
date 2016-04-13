# app_config.py
from ConfigParser import SafeConfigParser


class AppConfig(object):
    PROJECT_DIR = None
    TI_INSTALL_DIR = None
    # TODO: Link CURRENT_PROJECT_* with a @property.setter which automatically sets all from one, (e.g., set all using just folder dir)
    CURRENT_PROJECT_PATH = None  # Path to base of currently open project's folder
    CURRENT_PROJECT_NAME = None
    CURRENT_PROJECT_CONFIG = None

    def __init__(self):
        super(AppConfig, self).__init__()

    @classmethod
    def load_application_config(cls):
        config_parser = SafeConfigParser()
        config_parser.read(".application")
        cls.PROJECT_DIR = config_parser.get("info", "default_project_dir")
        cls.TI_INSTALL_DIR = config_parser.get("info", "ti_install_dir")

    # TODO: class method for writing to application config file
