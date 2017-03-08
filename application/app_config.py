# app_config.py
from ConfigParser import SafeConfigParser, NoSectionError, NoOptionError
import os

application_name = "SantosGUI"

class AppConfig(object):
    DEFAULT_PROJECT_DIR = os.path.realpath(os.path.join(os.path.expanduser('~'), "Documents", application_name, "project_dir"))
    CURRENT_PROJECT_PATH = None

def get_default_project_dir():
    return AppConfig.DEFAULT_PROJECT_DIR

def create_default_project_dir():
    if not os.path.exists(AppConfig.DEFAULT_PROJECT_DIR):
        os.makedirs(AppConfig.DEFAULT_PROJECT_DIR)

def get_project_path():
    return AppConfig.CURRENT_PROJECT_PATH

def get_config_path():
    if AppConfig.CURRENT_PROJECT_PATH:
        return os.path.join(AppConfig.CURRENT_PROJECT_PATH, "config.cfg")
    return None

def get_identifier():
    config_path = get_config_path()
    if config_path:
        return get_config_with_sections(config_path, "info", "identifier")
    return None

def get_project_video_path():
    config_path = get_config_path()
    if config_path:
        video = get_config_with_sections(config_path, "video", "name")
        if video:
            return os.path.join(get_project_path(), video)
        else:
            print("ERR: project_video(): Couldn't get video")
    return None

def update_config_with_sections(config_path, section, option, value):
    """
    Updates a single value in the current open project's configuration file.
    Writes nothing and returns -1 if no project currently open. Creates sections
    in the config file if they do not already exist.

    Args:
        config_path (str): Path to the config file
        section (str): Name of the section to write new option-value pair to write.
        option (str): Name of the option to write/update.
        value (str): Value to write/update assocaited with the specified option.
    """
    if not os.path.exists(config_path):
        print("ERR [update_config_with_sections()]: File {} does not exist.".format(config_path))
        return -1
    cfp = SafeConfigParser()
    cfp.read(config_path)
    if section not in cfp.sections():  # If the given section does not exist,
        cfp.add_section(section)        # then create it.
    cfp.set(section, option, value)  # Set the option-value pair
    with open(config_path, "wb") as cfg_file:
        cfp.write(cfg_file)  # Write changes


def get_config_with_sections(config_path, section, option):
    """
    Checks the configuration file for the specified option
    in the specified section. If it exists, this returns <value>. If it does not
    exist, this returns None.

    Args:
        config_path (str): Path to the config file to check
        section (str): Name of the section to check for option.
        option (str): Name of the option check/return.
    """
    if config_path == None:
        print("ERR [get_config_with_sections()]: config_path was None.")
        return None
    if not os.path.exists(config_path):
        print("ERR [get_config_with_sections()]: File {} does not exist.".format(config_path))
        return None
    cfp = SafeConfigParser()
    cfp.read(config_path)
    try:
        value = cfp.get(section, option)
    except NoSectionError:
        return None
    except NoOptionError:
        return None
    else:
        return value

def get_config_section(config_path, section):
    """
    Checks the configuration file for the specified option
    in the specified section. If it exists, this returns dict_of_data. If it does not
    exist, this returns None.

    Args:
        config_path (str): Path to the config file to check
        section (str): Name of the section whose data should be returned.
    """
    if not os.path.exists(config_path):
        print("ERR [get_config_section()]: File {} does not exist.".format(config_path))
        return None
    cfp = SafeConfigParser()
    cfp.read(config_path)
    try:
        tuples = cfp.items(section)
    except NoSectionError:
        print("ERR [get_config_section()]: Section {} is not available in {}.".format(section, config_path))
        return None
    else:
        d = {}
        for (key, value) in tuples:
            d[key] = value
        return d


def config_section_exists(config_path, section):
    """
    Checks the currently open project's configuration file for the section. If it exists,
    this returns True. If it does not exist, this returns False.

    Args:
        config_path (str): Path to the config file.
        section (str): Name of the section to check existance of.
    """
    cfp = SafeConfigParser()
    cfp.read(config_path)
    if section in cfp.sections():  # If the given section exists,
        return True                # then return True.
    else:                          # Otherwise,
        return False               # then return False

def update_config_without_sections(config_path, update_dict):
    """helper function to edit cfg files that look like tracking.cfg

    update_dict: i.e. {'nframes': 10, 'video-filename': 'video.avi'}
    """
    unused_keys = update_dict.keys()
    with open(config_path, 'r') as rf:
        lines = rf.readlines()
    with open(config_path, 'w') as wf:
        for line in lines:
            line_param = line.split('=')[0].strip()
            if line_param in update_dict.keys():
                wf.write("{} = {}\n".format(line_param, update_dict[line_param]))
                unused_keys.remove(line_param)
            else:
                wf.write(line)
        for unused_key in unused_keys:
            wf.write("{} = {}\n".format(unused_key, update_dict[unused_key]))


def get_config_without_sections(config_path):
    """helper function to get params and their values of cfg files that look like tracking.cfg

    get_dict: params to their values, as a dictionary
    """
    get_dict = {}
    with open(config_path, 'r') as rf:
        lines = rf.readlines()
        for line in lines:
            # if not a comment line
            if line[0] != "#":
                line_param = line.split('=')[0].strip()
                line_value = line.split('=')[1].strip()
                get_dict[line_param] = line_value
    return get_dict

