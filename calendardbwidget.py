from datetime import datetime, timedelta, time
from PyQt4 import QtGui as qtgui
from PyQt4 import QtCore as qtcore
from PyQt4.Qt import Qt

from worktimedialog import WorktimeDialog
from specialdaydialog import SpecialDayDialog
from neweventdialog import NewEventDialog
from database import WEEKDAYS


def sec_to_hstr(time, fmt='{h:02}:{m:02}'):
    if isinstance(time, timedelta):
        time = time.total_seconds()
    h, r = divmod(time, 3600)
    m, s = divmod(r, 60)
    return fmt.format(h=int(h), m=int(m), s=int(s))


class CalendarDBWidget(qtgui.QWidget):
    def __init__(self, db, parent=None):
        qtgui.QWidget.__init__(self, parent=parent)

        self.db = db

        self.specialdaydialog = SpecialDayDialog(self.db, self)

        self.worktimedialog = WorktimeDialog(db)

        self.neweventdialog = NewEventDialog(db, self)

        lay_tools = qtgui.QVBoxLayout()

        self.constraints = qtgui.QPushButton(self.style().standardIcon(qtgui.QStyle.SP_DialogApplyButton), None)
        self.constraints.clicked.connect(self.show_worktime)

        self.refresh = qtgui.QPushButton(self.style().standardIcon(qtgui.QStyle.SP_BrowserReload), None)
        self.refresh.clicked.connect(self.update)

        lay_tools.addWidget(self.refresh)
        lay_tools.addWidget(self.constraints)
        lay_tools.addStretch()

        lay_grid = qtgui.QGridLayout()

        self.calendar = qtgui.QCalendarWidget()
        self.calendar.setFirstDayOfWeek(1)
        self.calendar.currentPageChanged.connect(self.cal_browse)
        self.calendar.selectionChanged.connect(self.cal_select)
        self.calendar.activated.connect(self.specialday)

        lay_current = qtgui.QVBoxLayout()
        box_current = qtgui.QGroupBox("Today")
        box_current.setLayout(lay_current)
        box_current.setFlat(False)

        lay_tmp = qtgui.QHBoxLayout()
        self.button_checkin = qtgui.QPushButton("Check IN")
        self.button_checkout = qtgui.QPushButton("Check OUT")
        self.button_checkin.setDisabled(True)
        self.button_checkout.setDisabled(True)
        self.button_checkin.setStyleSheet("background-color: pink")
        self.button_checkout.setStyleSheet("background-color: pink")
        self.button_checkin.clicked.connect(lambda: self.new_event(1))
        self.button_checkout.clicked.connect(lambda: self.new_event(2))
        lay_tmp.addWidget(self.button_checkin)
        lay_tmp.addWidget(self.button_checkout)
        lay_current.addLayout(lay_tmp)

        self.current_state = qtgui.QLabel('--')
        self.current_state.setAlignment(Qt.AlignCenter);
        lay_current.addWidget(self.current_state)

        lay_day = qtgui.QVBoxLayout()
        self.box_day = qtgui.QGroupBox("00. 00. 0000")
        self.box_day.setLayout(lay_day)
        self.box_day.setFlat(False)

        self.neweventbutton = qtgui.QPushButton(self.style().standardIcon(qtgui.QStyle.SP_VistaShield), None)
        self.neweventbutton.clicked.connect(self.show_newevent)
        lay_day.addWidget(self.neweventbutton)

        self.day_events = qtgui.QListWidget()
        lay_day.addWidget(self.day_events)

        shortcut = qtgui.QShortcut(qtgui.QKeySequence(Qt.Key_Delete), self.day_events)
        shortcut.activated.connect(self.delete_event)

        self.day_hours = qtgui.QLabel('n/a')
        lay_day.addWidget(self.day_hours)

        lay_week = qtgui.QFormLayout()
        self.box_week = qtgui.QGroupBox("Week")
        self.box_week.setLayout(lay_week)
        self.box_week.setFlat(False)

        self.week_hours = qtgui.QLabel('n/a')
        self.week_total = qtgui.QLabel('n/a')
        self.week_dayh = {}
        for d in WEEKDAYS:
            label = qtgui.QLabel('n/a')
            self.week_dayh[d] = label
            lay_week.addRow(d + ':', label)
        lay_week.addRow('', qtgui.QWidget())
        lay_week.addRow('Total:', self.week_total)
        lay_week.addRow('Desired:', self.week_hours)

        lay_year = qtgui.QVBoxLayout()
        self.box_year = qtgui.QGroupBox("Year")
        self.box_year.setLayout(lay_year)
        self.box_year.setFlat(False)

        self.vacation_taken = qtgui.QLabel('Vacation...')
        lay_year.addWidget(self.vacation_taken)

        lay_total = qtgui.QVBoxLayout()
        self.box_total = qtgui.QGroupBox("Total")
        self.box_total.setLayout(lay_total)
        self.box_total.setFlat(False)

        self.total_start = qtgui.QDateTimeEdit()
        lay_total.addWidget(self.total_start)
        self.total_start.setDisplayFormat("dd.MM.yyyy")
        self.total_start.setCalendarPopup(True)
        self.total_start.setDate(db.get_misc('start_total', type='date'))
        self.total_start.dateChanged.connect(self.change_start)

        self.total_end = qtgui.QDateTimeEdit()
        lay_total.addWidget(self.total_end)
        self.total_end.setDisplayFormat("dd.MM.yyyy")
        self.total_end.setCalendarPopup(True)
        now = datetime.now()
        self.total_end.setDate(now - timedelta(now.weekday() + 1))
        self.total_end.dateChanged.connect(self.change_start)

        self.total_balance = qtgui.QLabel('Work balance: ---')
        lay_total.addWidget(self.total_balance)

        lay_grid.addWidget(self.calendar, 0, 0)
        lay_grid.addWidget(box_current, 0, 1)
        lay_grid.addWidget(self.box_day, 1, 0)
        lay_grid.addWidget(self.box_week, 1, 1)
        lay_grid.addWidget(self.box_year, 2, 0)
        lay_grid.addWidget(self.box_total, 2, 1)

        lay_tmp = qtgui.QHBoxLayout()
        lay_tmp.addLayout(lay_tools)
        lay_tmp.addLayout(lay_grid)

        self.setLayout(lay_tmp)

        self.update()

    def show_worktime(self):
        self.worktimedialog.show()
        self.worktimedialog.raise_()

    def show_newevent(self):
        self.neweventdialog.set_date(self.calendar.selectedDate())
        self.neweventdialog.show()

    def new_event(self, code):
        self.db.new_event(code)
        self.update()

    def delete_event(self):
        if not self.day_events.hasFocus():
            return

        n = len(self.day_events.selectedItems())
        if n == 0:
            return

        box = qtgui.QMessageBox()
        box.setText("Really delete event(s)?")
        box.setText("Do you really want to delete {} events?".format(n))
        box.setStandardButtons(qtgui.QMessageBox.Yes | qtgui.QMessageBox.No)
        box.setDefaultButton(qtgui.QMessageBox.No)
        if box.exec() == qtgui.QMessageBox.Yes:
            for ev in self.day_events.selectedItems():
                self.db.delete_event(ev.data(1))
            self.update()

    def update(self):
        self.update_calendar()
        self.update_state()
        self.update_day()
        self.update_week()
        self.update_year()
        self.update_total()

    def update_calendar(self):
        format = qtgui.QTextCharFormat()
        self.calendar.setDateTextFormat(qtcore.QDate(-4713, 1, 1), format)

        format.setFontWeight(qtgui.QFont.Black)
        format.setForeground(qtgui.QColor('blue'))
        format.setBackground(qtgui.QColor('lightblue'))
        self.calendar.setDateTextFormat(datetime.now(), format)

        format = qtgui.QTextCharFormat()

        for date, tid, name, tstr, _, color in self.db.specialdays():
            format.setBackground(qtgui.QColor(color))
            self.calendar.setDateTextFormat(date, format)

    def update_state(self):
        dbstate = self.db.get_state()
        if dbstate is None:
            last_id = 2
        else:
            last_event, last_id, last_description = dbstate

        if last_id == 1:
            self.button_checkin.setDisabled(True)
            self.button_checkout.setDisabled(False)
            self.button_checkin.setStyleSheet("background-color: pink")
            self.button_checkout.setStyleSheet("background-color: red")
        elif last_id == 2:
            self.button_checkin.setDisabled(False)
            self.button_checkout.setDisabled(True)
            self.button_checkin.setStyleSheet("background-color: red")
            self.button_checkout.setStyleSheet("background-color: pink")
        else:
            raise RuntimeError("Invalid event code: {} ({}) at {}".format(last_id, last_description, last_event))

        if dbstate is None:
            self.current_state.setText('checked out since')
        else:
            last_description = last_description.replace('check-', 'checked ').replace('in', 'IN').replace('out', 'OUT')

            if last_event.date() == datetime.now().date():
                last_event_str = last_event.strftime('%H:%M')
            elif (last_event + timedelta(1, 0, 0)).date() == datetime.now().date():
                last_event_str = 'yesterday, ' + last_event.strftime('%H:%M')
            else:
                last_event_str = last_event.strftime('%d.%m.%Y, %H:%M')

            self.current_state.setText('{} since {}'.format(last_description, last_event_str))

    def update_day(self):
        date = self.calendar.selectedDate()
        self.box_day.setTitle(date.toString())
        self.day_events.clear()
        times = []
        for date, str in self.db.get_events(date.toPyDate()):
            item = qtgui.QListWidgetItem("{} {}".format(date.strftime('%H:%M'), str), self.day_events)
            item.setData(1, date)
            times.append(date)
        totaltime = sum([b - a for a, b in zip(times[0::2], times[1::2])], timedelta(0))
        if len(times) % 2 == 1:
            totaltime += datetime.now() - times[-1]
        s = totaltime.total_seconds()
        h, r = divmod(s, 3600)
        m, s = divmod(r, 60)
        self.day_hours.setText('Total work time: {:02}:{:02}'.format(int(h), int(m)))

    def update_week(self):
        date = self.calendar.selectedDate()
        self.box_week.setTitle('Week: {}, {}'.format(*date.weekNumber()))

        date = date.toPyDate()

        beginning_of_week = date - timedelta(date.weekday())

        now = datetime.now()

        weektime = timedelta(0)
        for n, daystr in enumerate(WEEKDAYS):
            day = beginning_of_week + timedelta(n)
            if day == now.date():
                worktime = self.db.get_worktime(day, now)
            else:
                worktime = self.db.get_worktime(day)
            weektime += worktime

            self.week_dayh[daystr].setText(sec_to_hstr(worktime))

        self.week_total.setText(sec_to_hstr(weektime))
        self.week_hours.setText(sec_to_hstr(self.db.get_desired_weektime(beginning_of_week)))

    def update_year(self):
        year = self.calendar.yearShown()
        date = datetime(year, 1, 1)
        self.box_year.setTitle(date.strftime('%Y'))
        vac_taken = self.db.get_vacation(year)
        vac_total = self.db.get_constraints(datetime(year, 12, 31))['vacationdays_per_year'][0]
        self.vacation_taken.setText('Vacation days taken: {} / {}'.format(vac_taken, vac_total))

    def update_total(self):
        date = self.total_start.date().toPyDate()
        until = self.total_end.date().toPyDate()
        balance, actual, target = timedelta(), timedelta(), timedelta()
        while date <= until:
            target += self.db.get_desired_weektime(date)
            actual += self.db.get_actual_weektime(date)
            date += timedelta(7)
        balance = actual - target
        if balance > timedelta():
            self.total_balance.setText("Work balance: <font color='green'>{}</font>".format(balance))
        else:
            self.total_balance.setText("Work balance: <font color='red'>-{}</font>".format(-balance))


    def cal_browse(self):
        self.update_year()

    def cal_select(self):
        self.update_day()
        self.update_week()
        self.update_year()

    def specialday(self):
        date = self.calendar.selectedDate()
        self.specialdaydialog.set_date(date)
        self.specialdaydialog.exec()
        self.update()

    def change_start(self):
        date = self.total_start.date().toPyDate()
        beginning_of_week = date - timedelta(date.weekday())
        self.total_start.setDate(beginning_of_week)
        self.db.set_misc('start_total', beginning_of_week)
        self.update_total()
