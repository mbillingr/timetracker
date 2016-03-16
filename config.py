import os
from configparser import ConfigParser
from appdirs import user_data_dir


userdir = user_data_dir('timetracker')
print('userdir: ', userdir)

if not os.path.exists(userdir):
    os.makedirs(userdir)


config_file = os.path.join(userdir, 'config.ini')

config = ConfigParser()
config.read(config_file)
dirty_flag = False


def initialize(key, value, section='DEFAULT'):
    global dirty_flag
    section = config[section]
    if key in section:
        return
    section[key] = value
    dirty_flag = True


def write():
    print('writing config')
    with open(config_file, 'w') as cf:
        config.write(cf)


def get(key, section='DEFAULT'):
    return config[section][key]


initialize('database', os.path.join(userdir, 'worktime.db3'))
initialize('gui_style', 'plastique')

if dirty_flag:
    write()
