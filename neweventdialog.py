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


from datetime import datetime, timedelta, time
from PyQt4 import QtGui as qtgui
from PyQt4 import QtCore as qtcore
from PyQt4.Qt import Qt
import re


from database import WEEKDAYS, WEEKDAYS_SHORT


class NewEventDialog(qtgui.QDialog):
    def __init__(self, db, parent=None):
        qtgui.QDialog.__init__(self, parent=parent)
        self.db = db
        self.date = None

        lay_h = qtgui.QHBoxLayout()
        lay_v = qtgui.QVBoxLayout()

        self.datetime = qtgui.QDateTimeEdit()

        self.check_in = qtgui.QRadioButton('check in')
        self.check_out = qtgui.QRadioButton('check out')

        self.add = qtgui.QPushButton(self.style().standardIcon(qtgui.QStyle.SP_DialogOkButton), None)

        lay_v.addWidget(self.check_in)
        lay_v.addWidget(self.check_out)

        lay_h.addWidget(self.datetime)
        lay_h.addLayout(lay_v)
        lay_h.addWidget(self.add)

        self.setLayout(lay_h)

        self.add.clicked.connect(self.add_event)

    def add_event(self):
        date = self.datetime.dateTime().toPyDateTime()
        if self.check_in.isChecked():
            self.db.new_event(1, date)
        elif self.check_out.isChecked():
            self.db.new_event(2, date)

    def set_date(self, date):
        self.datetime.setDate(date)
