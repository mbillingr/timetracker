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
# Copyright (C) <2016> Martin Billinger


import re
import datetime
import calendar
from PyQt4 import QtGui as qtgui
from PyQt4 import QtCore as qtcore
from PyQt4.Qt import Qt
import numpy as np
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle
import matplotlib.dates as mdates
from matplotlib import gridspec
import seaborn


from database import WEEKDAYS, WEEKDAYS_SHORT


class StatisticsDialog(qtgui.QDialog):
    def __init__(self, db, parent=None):
        qtgui.QDialog.__init__(self, parent=parent)
        self.db = db
        self.date = None

        lay_h = qtgui.QHBoxLayout()

        self.punchcard = PlotPunchcard(db)
        self.overview = PlotOverview(db)

        self.tabs = qtgui.QTabWidget()
        self.tabs.addTab(self.punchcard, "Punch card")
        self.tabs.addTab(self.overview, "Yearly overview")

        self.tabs.currentChanged.connect(self.changetab)

        lay_h.addWidget(self.tabs)

        self.setLayout(lay_h)
        self.tabs.currentWidget().plot()

    def changetab(self, index):
        self.tabs.currentWidget().plot()


class PlotPunchcard(FigureCanvas):
    def __init__(self, db):
        self.db = db
        self.fig = Figure()
        super().__init__(self.fig)

    def plot(self):
        events = self.db.get_events()
        days = np.array([e[0].weekday() for e in events])
        times = np.array([e[0].time() for e in events])
        types = np.array([e[1] for e in events])

        here = np.zeros((7, 24 * 60))
        for a, b, c, d in zip(times[types=='check-in'], times[types=='check-out'], days[types=='check-in'], days[types=='check-out']):

            if c == d:
                a = a.hour * 60.0 + a.minute
                b = b.hour * 60.0 + b.minute

                here[c][a:b] += 1
            else:
                raise NotImplementedError("Punchcard: Checkout not on the same day is not supported")

        here = here.reshape(7, -1, 15).mean(-1)
        here /= np.max(here)

        self.fig.clf()
        ax = self.fig.add_subplot(111)

        for i, h in enumerate(here):
            ax.bar(np.arange(len(h)), h, width=1.0, bottom=i*2 - h*0.5)

        l = np.linspace(0, len(h), 7)
        ax.set_xticks(l)
        ax.set_xticklabels(['{:02d}:00'.format(int(i * 24 / len(h))) for i in l])
        ax.set_xlim(0, len(h))

        ax.set_yticks([0, 2, 4, 6, 8, 10, 12])
        ax.set_yticklabels(['Monday', 'Tuesday', 'Wednesday', 'Thirsday', 'Friday', 'Saturday', 'Sunday'])

        ax.set_ylim(-1, 13)
        ax.invert_yaxis()


class PlotOverview(qtgui.QWidget):
    def __init__(self, db):
        self.db = db
        self.fig = Figure()
        self.canvas = FigureCanvas(self.fig)
        super().__init__()

        lay_v = qtgui.QVBoxLayout()
        self.setLayout(lay_v)

        self.year = qtgui.QComboBox()
        self.year.currentIndexChanged.connect(self.plot)

        lay_h = qtgui.QHBoxLayout()
        lay_h.addWidget(self.year)
        lay_h.addStretch(1)
        lay_v.addLayout(lay_h)
        lay_v.addWidget(self.canvas)

        self.update()

    def update(self):
        constraints = self.db.get_constraints()
        current_year = self.year.currentText()
        self.year.clear()
        years = [y for y in range(min(constraints['start_date']).year, datetime.datetime.now().year + 1)]
        self.year.addItems([str(y) for y in years])
        try:
            self.year.setCurrentIndex(years.index(current_year))
        except ValueError:
            self.year.setCurrentIndex(len(years) - 1)

    def plot(self):
        self.fig.clf()
        ax = self.fig.add_subplot(111)

        worked = np.zeros((12, 34)) + np.nan

        year = int(self.year.currentText())
        for month in range(12):
            for day in range(calendar.monthrange(year, month + 1)[1]):
                date = datetime.date(year, month + 1, day + 1)
                if date < datetime.datetime.now().date():
                    t = self.db.get_worktime(date).total_seconds() / 60.0 - self.db.get_desiredtime(date)
                    worked[month, day] = t
                    ax.text(day, month, re.sub('0(?=[.])', '', ('{:.1f}'.format(t / 60))), ha='center', va='center')

        worked[:, 32:] = np.nansum(worked[:, :31], axis=1, keepdims=True)

        for month in range(12):
            ax.text(32.5, month, re.sub('0(?=[.])', '', ('{:.1f}'.format(worked[month, -1] / 60))), ha='center', va='center')

        ax.imshow(worked, vmin=-12*60, vmax=12*60, interpolation='none', cmap='coolwarm')
        ax.set_xticks(np.arange(31))
        ax.set_yticks(np.arange(12))
        ax.set_xticklabels(1 + np.arange(31))
        ax.set_yticklabels(calendar.month_name[1:])

        self.fig.tight_layout()
        self.canvas.draw()



