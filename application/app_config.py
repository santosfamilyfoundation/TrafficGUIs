# app_config.py
from ConfigParser import SafeConfigParser
import os


class AppConfig(object):
    PROJECT_DIR = None
    TI_INSTALL_DIR = None
    # TODO: Link CURRENT_PROJECT_* with a @property.setter which automatically sets all from one, (e.g., set all using just folder dir)
    CURRENT_PROJECT_PATH = None  # Path to base of currently open project's folder
    CURRENT_PROJECT_NAME = None
    CURRENT_PROJECT_CONFIG = None  # Path
    CURRENT_PROJECT_VIDEO_PATH = None

    def __init__(self):
        super(AppConfig, self).__init__()

    @classmethod
    def load_application_config(cls):
        config_parser = SafeConfigParser()
        config_parser.read(os.path.join(os.path.dirname(os.path.realpath(__file__)), ".application"))
        cls.PROJECT_DIR = config_parser.get("info", "default_project_dir")
        cls.TI_INSTALL_DIR = config_parser.get("info", "ti_install_dir")

    # TODO: class method for writing to application config file

def update_project_cfg(section, option, value):
    """
    Updates a single value in the current open project's configuration file.
    Writes nothing and returns -1 if no project currently open. Creates sections
    in the config file if they do not already exist.

    Args:
        section (str): Name of the section to write new option-value pair to write.
        option (str): Name of the option to write/update.
        value (str): Value to write/update assocaited with the specified option.
    """
    if not AppConfig.CURRENT_PROJECT_CONFIG:
        return -1
    cfp = SafeConfigParser()
    cfp.read(AppConfig.CURRENT_PROJECT_CONFIG)
    if section not in cfp.sections():  # If the given section does not exist,
        cfp.add_section(section)        # then create it.
    cfp.set(section, option, value)  # Set the option-value pair
    with open(AppConfig.CURRENT_PROJECT_CONFIG, "wb") as cfg_file:
        cfp.write(cfg_file)  # Write changes


def check_project_cfg_option(section, option):
    """
    Checks the currently open project's configuration file for the specified option
    in the specified section. If it exists, this returns (True, <value>). If it does not
    exist, this returns (False, None).

    Args:
        section (str): Name of the section to check for option.
        option (str): Name of the option check/return.
    """
    cfp = SafeConfigParser()
    cfp.read(AppConfig.CURRENT_PROJECT_CONFIG)
    try:
        value = cfp.get(section, option)
    except NoSectionError:
        print("ERR [check_project_cfg_option()]: Section {} is not available in {}.".format(section, AppConfig.CURRENT_PROJECT_CONFIG))
        return (False, None)
    except NoOptionError:
        print("Option {} is not available in {}.".format(option, AppConfig.CURRENT_PROJECT_CONFIG))
        return (False, None)
    else:
        return (True, value)


def check_project_cfg_section(section):
    """
    Checks the currently open project's configuration file for the section. If it exists,
    this returns True. If it does not exist, this returns False.

    Args:
        section (str): Name of the section to check existance of.
    """
    cfp = SafeConfigParser()
    cfp.read(AppConfig.CURRENT_PROJECT_CONFIG)
    if section in cfp.sections():  # If the given section exists,
        return True                # then return True.
    else:                          # Otherwise,
        return False               # then return False