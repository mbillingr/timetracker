# This file is part of Timetracker.
#
# Timetracker is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Timetracker is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Timetracker.  If not, see <http://www.gnu.org/licenses/>.
#
# Copyright (C) <2015-2016> Martin Billinger


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
