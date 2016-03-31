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


import datetime
from PyQt4 import QtGui as qtgui
from PyQt4 import QtCore as qtcore
from PyQt4.Qt import Qt
import numpy as np
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle
import matplotlib.dates as mdates
import seaborn


from database import WEEKDAYS, WEEKDAYS_SHORT


class StatisticsDialog(qtgui.QDialog):
    def __init__(self, db, parent=None):
        qtgui.QDialog.__init__(self, parent=parent)
        self.db = db
        self.date = None

        lay_h = qtgui.QHBoxLayout()

        self.punchcard = PlotPunchcard(db)
        self.punchcard2 = PlotPunchcard(db)

        self.tabs = qtgui.QTabWidget()
        self.tabs.addTab(self.punchcard, "Punch card")
        self.tabs.addTab(self.punchcard2, "Punch card 2")

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
