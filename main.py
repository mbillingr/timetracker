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
