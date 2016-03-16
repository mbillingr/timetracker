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


class TimeSpinBox(qtgui.QSpinBox):
    def __init__(self, parent=None):
        qtgui.QSpinBox.__init__(self, parent=parent)

        self.setMinimum(0)
        self.setMaximum(999999)
        self.setSingleStep(15)

    def textFromValue(self, value):
        h, m = divmod(value, 60)
        return '{}:{:02}'.format(h, m)

    def valueFromText(self, text):
        s = [i if len(i) > 0 else 0 for i in text.split(':')]

        if len(s) == 1:
            return int(s[0]) * 60
        elif len(s) == 2:
            return int(s[0]) * 60 + int(s[1])

    def validate(self, text, pos):
        if re.fullmatch('[0123456789]*:?[0123456789]*', text):
            return qtgui.QValidator.Acceptable, text, pos
        return qtgui.QValidator.Invalid, text, pos


class MultiSpinBox(qtgui.QWidget):
    def __init__(self, n_boxes, parent=None):
        qtgui.QWidget.__init__(self, parent=parent)

        self.setLayout(qtgui.QHBoxLayout())

        self.spinboxes = [TimeSpinBox() for n in range(n_boxes)]
        for box in self.spinboxes:
            self.layout().addWidget(box)

    def set(self, *values):
        for s, v in zip(self.spinboxes, values):
            s.setValue(v)

    def values(self):
        return [s.value() for s in self.spinboxes]


class CheckSpin(qtgui.QWidget):
    def __init__(self, use_checkbox=True, parent=None):
        qtgui.QWidget.__init__(self, parent=parent)

        self.checkbox = qtgui.QCheckBox()
        self.spinbox = TimeSpinBox()

        self.setLayout(qtgui.QHBoxLayout())
        self.layout().addWidget(self.checkbox)
        self.layout().addWidget(self.spinbox)

        self.checkbox.setEnabled(use_checkbox)

        self.checkbox.setTristate(False)

    def set(self, value, allow_flex=None):
        if allow_flex is not None:
            self.checkbox.setChecked(allow_flex)
        self.spinbox.setValue(value)

    def value(self):
        if self.checkbox.isEnabled():
            return self.spinbox.value(), self.checkbox.isChecked()
        else:
            return self.spinbox.value()


class WorktimeDialog(qtgui.QDialog):
    def __init__(self, db, parent=None):
        qtgui.QDialog.__init__(self, parent=parent)

        self.db = db

        self.list = qtgui.QListWidget()
        self.list.itemSelectionChanged.connect(self.item_selected)

        self.date = qtgui.QDateTimeEdit()
        self.date.setDisplayFormat("dd.MM.yyyy")
        self.date.setCalendarPopup(True)

        self.dayboxes = {ds: [TimeSpinBox() for n in range(3)] for ds in WEEKDAYS_SHORT}
        self.vac = qtgui.QSpinBox()
        self.flex = TimeSpinBox()

        self.new = qtgui.QPushButton(self.style().standardIcon(qtgui.QStyle.SP_FileDialogNewFolder), None)
        self.save = qtgui.QPushButton(self.style().standardIcon(qtgui.QStyle.SP_DialogSaveButton), None)

        self.save.clicked.connect(lambda: self.save_enty())

        lay_h = qtgui.QHBoxLayout()
        lay_h.addWidget(self.list)

        lay_f = qtgui.QGridLayout()
        lay_f.addWidget(qtgui.QLabel("Work"), 10, 1)
        lay_f.addWidget(qtgui.QLabel("Vacation"), 10, 2)
        lay_f.addWidget(qtgui.QLabel("Holiday"), 10, 3)
        for i, (day, ds) in enumerate(zip(WEEKDAYS, WEEKDAYS_SHORT)):
            lay_f.addWidget(qtgui.QLabel(day), 11 + i, 0)
            for j in range(3):
                lay_f.addWidget(self.dayboxes[ds][j], 11 + i, 1 + j)
                self.dayboxes[ds][j].valueChanged.connect(self.update_sums)

        lay_f.addWidget(qtgui.QLabel("Date"), 5, 0)
        lay_f.addWidget(self.date, 5, 1)

        lay_f.addWidget(qtgui.QLabel("Flexible"), 21, 0)
        lay_f.addWidget(self.flex, 21, 1)

        self.sums = [qtgui.QLabel("n/a"), qtgui.QLabel("n/a"), qtgui.QLabel("n/a")]

        lay_f.addWidget(self.sums[0], 25, 1)
        lay_f.addWidget(self.sums[1], 25, 2)
        lay_f.addWidget(self.sums[2], 25, 3)

        lay_f.addWidget(qtgui.QLabel("Vacation"), 31, 0)
        lay_f.addWidget(self.vac, 31, 1)

        lay_f.addWidget(self.save, 50, 1)
        lay_f.addWidget(self.new, 50, 2)

        lay_h.addLayout(lay_f)

        self.setLayout(lay_h)

        self.update()

    def update(self):
        self.list.clear()
        for d in self.db.get_constraints()['start_date']:
            item = qtgui.QListWidgetItem(d.strftime('%d. %m. %Y'), self.list)
            item.setData(1, d)

    def update_sums(self):
        sums = [0] * len(self.sums)
        sums[0] += self.flex.value()
        for ds in WEEKDAYS_SHORT:
            for i, box in enumerate(self.dayboxes[ds]):
                sums[i] += box.value()
        for s, l in zip(sums, self.sums):
            h, m = divmod(s, 60)
            l.setText('{}:{:02}'.format(h, m))

    def item_selected(self):
        date = self.list.currentItem().data(1)
        c = self.db.get_constraints(date)
        self.date.setDate(date)
        for day, ds in zip(WEEKDAYS, WEEKDAYS_SHORT):
            self.dayboxes[ds][0].setValue(c[day.lower()][0])
            self.dayboxes[ds][1].setValue(c[ds.lower() + '_vacation'][0])
            self.dayboxes[ds][2].setValue(c[ds.lower() + '_free'][0])
        self.flex.setValue(c['flexible'][0])
        self.vac.setValue(c['vacationdays_per_year'][0])
        self.update_sums()

    def save_enty(self):
        date = self.date.date()
        date = datetime.combine(date.toPyDate(), time())

        c = {'start_date': date,
             'flexible': self.flex.value(),
             'vacationdays_per_year': self.vac.value()}

        for day, ds in zip(WEEKDAYS, WEEKDAYS_SHORT):
            c[day.lower()] = self.dayboxes[ds][0].value()
            c[ds.lower() + '_vacation'] = self.dayboxes[ds][1].value()
            c[ds.lower() + '_free'] = self.dayboxes[ds][2].value()

        self.db.save_constraint(c)
        self.update()

