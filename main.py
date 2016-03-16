"""Timetracker is a small GUI program for tracking time at work.

Timetracker is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Timetracker is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Timetracker.  If not, see <http://www.gnu.org/licenses/>.

Copyright (C) <2015-2016> Martin Billinger
"""
if __name__ == '__main__':
    print(__doc__)


import sys
from PyQt4 import QtGui as qtgui

from calendardbwidget import CalendarDBWidget
from database import Database
import config


NAME = 'Time Tracker'


def main():
    app = qtgui.QApplication(sys.argv)
    app.setApplicationName(NAME)
    app.setStyle(config.get('gui_style'))

    db = Database(config.get('database'))#':memory:')

    w = CalendarDBWidget(db)
    w.setWindowTitle(NAME)
    w.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
