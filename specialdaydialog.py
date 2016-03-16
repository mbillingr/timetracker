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


class SpecialDayDialog(qtgui.QDialog):
    def __init__(self, db, parent=None):
        qtgui.QDialog.__init__(self, parent=parent)
        self.db = db
        self.date = None

        lay_h = qtgui.QHBoxLayout()

        self.datelabel = qtgui.QLabel('date')
        self.daytype = qtgui.QComboBox()
        self.text = qtgui.QLineEdit()
        self.delete = qtgui.QPushButton(self.style().standardIcon(qtgui.QStyle.SP_DialogCloseButton), None)

        lay_h.addWidget(self.delete)
        lay_h.addWidget(self.datelabel)
        lay_h.addWidget(self.daytype)
        lay_h.addWidget(self.text)

        self.daytype.addItem('---')
        for index, text, color in db.get_daycodes():
            self.daytype.addItem(text)

        self.setLayout(lay_h)

        self.finished.connect(self.save_date)
        self.delete.clicked.connect(self.delete_date)

    def set_date(self, date):
        self.date = date
        self.datelabel.setText(date.toString())
        info = self.db.get_specialday(date.toPyDate())

        if info is None:
            self.daytype.setCurrentIndex(0)
            self.text.setText('')
        else:
            code, text = info
            self.daytype.setCurrentIndex(code)
            self.text.setText(text)

    def save_date(self):
        print(self.daytype.currentIndex())
        if self.daytype.currentIndex() == 0:
            self.db.del_specialday(self.date.toPyDate())
        else:
            self.db.set_specialday(self.date.toPyDate(), self.daytype.currentIndex(), self.text.text())

    def delete_date(self):
        self.daytype.setCurrentIndex(0)
        self.accept()

