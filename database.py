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


from datetime import datetime, time, timedelta
import sqlite3


WEEKDAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
WEEKDAYS_SHORT = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']


class Database:
    def __init__(self, dbfile='arbeitszeit.db3'):
        self.version = '0.2'
        self.con = sqlite3.connect(dbfile, detect_types=sqlite3.PARSE_DECLTYPES)

        cur = self.con.cursor()

        if not self.check_table('misc'):
            cur.execute('CREATE TABLE misc (key TEXT UNIQUE, value TEXT)')
            cur.execute("INSERT INTO misc VALUES ('start_total', date('2000-01-01'))")
            cur.execute("INSERT INTO misc VALUES ('db_version', ?)", [self.version])

        if not self.check_table('events'):
            cur.execute('CREATE TABLE events (date TIMESTAMP PRIMARY KEY, fk_code INT)')

        if not self.check_table('eventcodes'):
            cur.execute('CREATE TABLE eventcodes (pk_code INT PRIMARY KEY, description TEXT)')
            cur.execute('INSERT INTO eventcodes (pk_code, description) VALUES (1, "check-in")')
            cur.execute('INSERT INTO eventcodes (pk_code, description) VALUES (2, "check-out")')

        if not self.check_table('specialdays'):
            cur.execute('CREATE TABLE specialdays (date TIMESTAMP UNIQUE, fk_code INT, text TEXT)')

            cur.execute('INSERT INTO specialdays (date, fk_code, text) VALUES (?, ?, ?)', [datetime(2014, 1, 1), 1, "Neujahr"])
            cur.execute('INSERT INTO specialdays (date, fk_code, text) VALUES (?, ?, ?)', [datetime(2014, 4, 18), 1, "Karfreitag"])
            cur.execute('INSERT INTO specialdays (date, fk_code, text) VALUES (?, ?, ?)', [datetime(2014, 4, 21), 1, "Ostermontag"])
            cur.execute('INSERT INTO specialdays (date, fk_code, text) VALUES (?, ?, ?)', [datetime(2014, 5, 1), 1, "Tag der Arbeit"])
            cur.execute('INSERT INTO specialdays (date, fk_code, text) VALUES (?, ?, ?)', [datetime(2014, 5, 29), 1, "Himmelfahrt"])
            cur.execute('INSERT INTO specialdays (date, fk_code, text) VALUES (?, ?, ?)', [datetime(2014, 6, 9), 1, "Pfingstmontag"])
            cur.execute('INSERT INTO specialdays (date, fk_code, text) VALUES (?, ?, ?)', [datetime(2014, 10, 3), 1, "Tag der Deutschen Einheit"])
            cur.execute('INSERT INTO specialdays (date, fk_code, text) VALUES (?, ?, ?)', [datetime(2014, 12, 24), 1, "Weihnachten"])
            cur.execute('INSERT INTO specialdays (date, fk_code, text) VALUES (?, ?, ?)', [datetime(2014, 12, 25), 1, "1. Weihnachtstag"])
            cur.execute('INSERT INTO specialdays (date, fk_code, text) VALUES (?, ?, ?)', [datetime(2014, 12, 26), 1, "2. Weihnachtstag"])
            cur.execute('INSERT INTO specialdays (date, fk_code, text) VALUES (?, ?, ?)', [datetime(2014, 12, 31), 1, "Silvester"])

            cur.execute('INSERT INTO specialdays (date, fk_code, text) VALUES (?, ?, ?)', [datetime(2015, 1, 1), 1, "Neujahr"])
            cur.execute('INSERT INTO specialdays (date, fk_code, text) VALUES (?, ?, ?)', [datetime(2015, 4, 3), 1, "Karfreitag"])
            cur.execute('INSERT INTO specialdays (date, fk_code, text) VALUES (?, ?, ?)', [datetime(2015, 4, 6), 1, "Ostermontag"])
            cur.execute('INSERT INTO specialdays (date, fk_code, text) VALUES (?, ?, ?)', [datetime(2015, 5, 1), 1, "Tag der Arbeit"])
            cur.execute('INSERT INTO specialdays (date, fk_code, text) VALUES (?, ?, ?)', [datetime(2015, 5, 14), 1, "Himmelfahrt"])
            cur.execute('INSERT INTO specialdays (date, fk_code, text) VALUES (?, ?, ?)', [datetime(2015, 5, 25), 1, "Pfingstmontag"])
            cur.execute('INSERT INTO specialdays (date, fk_code, text) VALUES (?, ?, ?)', [datetime(2015, 10, 3), 1, "Tag der Deutschen Einheit"])
            cur.execute('INSERT INTO specialdays (date, fk_code, text) VALUES (?, ?, ?)', [datetime(2015, 12, 24), 1, "Weihnachten"])
            cur.execute('INSERT INTO specialdays (date, fk_code, text) VALUES (?, ?, ?)', [datetime(2015, 12, 25), 1, "1. Weihnachtstag"])
            cur.execute('INSERT INTO specialdays (date, fk_code, text) VALUES (?, ?, ?)', [datetime(2015, 12, 26), 1, "2. Weihnachtstag"])
            cur.execute('INSERT INTO specialdays (date, fk_code, text) VALUES (?, ?, ?)', [datetime(2015, 12, 31), 1, "Silvester"])

            cur.execute('INSERT INTO specialdays (date, fk_code, text) VALUES (?, ?, ?)', [datetime(2016, 1, 1), 1, "Neujahr"])
            cur.execute('INSERT INTO specialdays (date, fk_code, text) VALUES (?, ?, ?)', [datetime(2016, 3, 25), 1, "Karfreitag"])
            cur.execute('INSERT INTO specialdays (date, fk_code, text) VALUES (?, ?, ?)', [datetime(2016, 3, 28), 1, "Ostermontag"])
            cur.execute('INSERT INTO specialdays (date, fk_code, text) VALUES (?, ?, ?)', [datetime(2016, 5, 1), 1, "Tag der Arbeit"])
            cur.execute('INSERT INTO specialdays (date, fk_code, text) VALUES (?, ?, ?)', [datetime(2016, 5, 5), 1, "Himmelfahrt"])
            cur.execute('INSERT INTO specialdays (date, fk_code, text) VALUES (?, ?, ?)', [datetime(2016, 5, 16), 1, "Pfingstmontag"])
            cur.execute('INSERT INTO specialdays (date, fk_code, text) VALUES (?, ?, ?)', [datetime(2016, 10, 3), 1, "Tag der Deutschen Einheit"])
            cur.execute('INSERT INTO specialdays (date, fk_code, text) VALUES (?, ?, ?)', [datetime(2016, 12, 24), 1, "Weihnachten"])
            cur.execute('INSERT INTO specialdays (date, fk_code, text) VALUES (?, ?, ?)', [datetime(2016, 12, 25), 1, "1. Weihnachtstag"])
            cur.execute('INSERT INTO specialdays (date, fk_code, text) VALUES (?, ?, ?)', [datetime(2016, 12, 26), 1, "2. Weihnachtstag"])
            cur.execute('INSERT INTO specialdays (date, fk_code, text) VALUES (?, ?, ?)', [datetime(2016, 12, 31), 1, "Silvester"])


        if not self.check_table('daycodes'):
            cur.execute('CREATE TABLE daycodes (pk_code INT PRIMARY KEY, description TEXT, color TEXT)')
            cur.execute('INSERT INTO daycodes VALUES (1, "holiday", "green")')
            cur.execute('INSERT INTO daycodes VALUES (2, "vacation", "cyan")')
            cur.execute('INSERT INTO daycodes VALUES (3, "sick leave", "yellow")')

        if not self.check_table('daynumbers'):
            cur.execute('CREATE TABLE daynumbers (nr INTEGER PRIMARY KEY, longname TEXT, shortname TEXT)')

            cur.execute('INSERT INTO daynumbers VALUES (1, "Montag", "Mo")')
            cur.execute('INSERT INTO daynumbers VALUES (2, "Dienstag", "Di")')
            cur.execute('INSERT INTO daynumbers VALUES (3, "Mittwoch", "Mi")')
            cur.execute('INSERT INTO daynumbers VALUES (4, "Donnerstag", "Do")')
            cur.execute('INSERT INTO daynumbers VALUES (5, "Freitag", "Fr")')
            cur.execute('INSERT INTO daynumbers VALUES (6, "Samstag", "Sa")')
            cur.execute('INSERT INTO daynumbers VALUES (7, "Sonntag", "So")')

        if not self.check_table('day_modes'):
            cur.execute('CREATE TABLE day_modes (mode INTEGER PRIMARY KEY, description TEXT)')
            cur.execute('INSERT INTO day_modes VALUES (0, "free")')
            cur.execute('INSERT INTO day_modes VALUES (1, "work day (normal)")')
            cur.execute('INSERT INTO day_modes VALUES (2, "work day (flexible)")')

        if not self.check_table('workplan'):
            cur.execute('CREATE TABLE workplan (start_date TIMESTAMP PRIMARY KEY, flexible INT DEFAULT 0,'
                        'monday INT DEFAULT 0, mon_vacation INT DEFAULT 0, mon_free INT DEFAULT 0, mon_workday BOOL DEFAULT 1,'
                        'tuesday INT DEFAULT 0, tue_vacation INT DEFAULT 0, tue_free INT DEFAULT 0, tue_workday BOOL DEFAULT 1,'
                        'wednesday INT DEFAULT 0, wed_vacation INT DEFAULT 0, wed_free INT DEFAULT 0, wed_workday BOOL DEFAULT 1,'
                        'thursday INT DEFAULT 0, thu_vacation INT DEFAULT 0, thu_free INT DEFAULT 0, thu_workday BOOL DEFAULT 1,'
                        'friday INT DEFAULT 0, fri_vacation INT DEFAULT 0, fri_free INT DEFAULT 0, fri_workday BOOL DEFAULT 1,'
                        'saturday INT DEFAULT 0, sat_vacation INT DEFAULT 0, sat_free INT DEFAULT 0, sat_workday BOOL DEFAULT 0,'
                        'sunday INT DEFAULT 0, sun_vacation INT DEFAULT 0, sun_free INT DEFAULT 0, sun_workday BOOL DEFAULT 0,'
                        'vacationdays_per_year INT)')
            cur.execute('INSERT INTO workplan (start_date, flexible, vacationdays_per_year) VALUES (?, 0, 0)', [datetime(2000, 1, 1)])

        self.con.commit()

        #self.generate_testdata()

        dbv = cur.execute("SELECT value FROM misc WHERE key='db_version'").fetchone()
        if dbv is None or dbv[0] != self.version:
            self.upgrade_database(dbv)

    def generate_testdata(self):
        cur = self.con.cursor()

        cur.execute('INSERT INTO events (date, fk_code) VALUES (?, ?)', [datetime(2015, 10, 5, 7, 45), 1])
        cur.execute('INSERT INTO events (date, fk_code) VALUES (?, ?)', [datetime(2015, 10, 5, 12, 0), 2])
        cur.execute('INSERT INTO events (date, fk_code) VALUES (?, ?)', [datetime(2015, 10, 5, 13, 0), 1])
        cur.execute('INSERT INTO events (date, fk_code) VALUES (?, ?)', [datetime(2015, 10, 5, 16, 0), 2])

        cur.execute('INSERT INTO events (date, fk_code) VALUES (?, ?)', [datetime(2015, 10, 6, 8, 0), 1])
        cur.execute('INSERT INTO events (date, fk_code) VALUES (?, ?)', [datetime(2015, 10, 6, 12, 0), 2])
        cur.execute('INSERT INTO events (date, fk_code) VALUES (?, ?)', [datetime(2015, 10, 6, 12, 45), 1])
        cur.execute('INSERT INTO events (date, fk_code) VALUES (?, ?)', [datetime(2015, 10, 6, 16, 0), 2])

        cur.execute('INSERT INTO events (date, fk_code) VALUES (?, ?)', [datetime(2015, 10, 7, 9, 0), 1])
        cur.execute('INSERT INTO events (date, fk_code) VALUES (?, ?)', [datetime(2015, 10, 7, 13, 0), 1])
        cur.execute('INSERT INTO events (date, fk_code) VALUES (?, ?)', [datetime(2015, 10, 7, 12, 0), 2])
        cur.execute('INSERT INTO events (date, fk_code) VALUES (?, ?)', [datetime(2015, 10, 7, 18, 0), 2])

        cur.execute('INSERT INTO events (date, fk_code) VALUES (?, ?)', [datetime(2015, 10, 8, 8, 30), 1])
        cur.execute('INSERT INTO events (date, fk_code) VALUES (?, ?)', [datetime(2015, 10, 8, 12, 0), 2])
        cur.execute('INSERT INTO events (date, fk_code) VALUES (?, ?)', [datetime(2015, 10, 8, 13, 0), 1])
        cur.execute('INSERT INTO events (date, fk_code) VALUES (?, ?)', [datetime(2015, 10, 8, 17, 15), 2])

        cur.execute('INSERT INTO specialdays (date, fk_code, text) VALUES (?, ?, ?)', [datetime(2015, 12, 23), 2, "Urlaub"])
        cur.execute('INSERT INTO specialdays (date, fk_code, text) VALUES (?, ?, ?)', [datetime(2015, 12, 22), 2, "Urlaub"])

        cur.execute('INSERT INTO workplan (start_date, flexible, monday, vacationdays_per_year) VALUES (?, 1848, 480, 24)', [datetime(2014, 11, 1)])

    def query_dict(self, query, sqlargs=None):
        cur = self.con.cursor()
        if sqlargs is None:
            cur.execute(query)
        else:
            cur.execute(query, sqlargs)

        result = {col[0]: [] for col in cur.description}

        for row in cur.fetchall():
            for c, v in zip(cur.description, row):
                result[c[0]].append(v)

        return result

    def get_misc(self, key, type=None):
        cur = self.con.cursor()
        if type == 'date':
            k, value = cur.execute("SELECT key, date(value) FROM misc WHERE key=?", [key]).fetchone()
            return datetime.strptime(value, "%Y-%m-%d")
        else:
            k, value = cur.execute("SELECT key, value FROM misc WHERE key=?", [key]).fetchone()
        return value

    def set_misc(self, key, value):
        cur = self.con.cursor()
        cur.execute("REPLACE INTO misc VALUES (?, ?)", (key, str(value)))
        self.con.commit()

    def check_table(self, table):
        cur = self.con.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", [table])
        r = cur.fetchone()
        if r is None:
            return False
        return r[0] == table

    def specialdays(self):
        cur = self.con.cursor()
        cur.execute("SELECT * FROM specialdays JOIN daycodes ON fk_code=pk_code")
        return cur.fetchall()

    def new_event(self, code, date=None):
        if date is None:
            date = datetime.now()
        cur = self.con.cursor()
        try:
            cur.execute('REPLACE INTO events (date, fk_code) VALUES (datetime(?), ?)', [date, code])
        except sqlite3.IntegrityError:
            print(date, code)
            raise
        self.con.commit()

    def delete_event(self, date):
        cur = self.con.cursor()
        cur.execute("DELETE FROM events WHERE datetime(date)=?", [date])
        self.con.commit()

    def get_state(self):
        cur = self.con.cursor()
        cur.execute("SELECT date, fk_code, description FROM events JOIN eventcodes on fk_code=pk_code ORDER BY datetime(date) DESC LIMIT 1")
        return cur.fetchone()

    def get_events(self, date=None):
        cur = self.con.cursor()
        if date is None:
            cur.execute('SELECT date, description FROM events JOIN eventcodes on fk_code=pk_code ORDER BY datetime(date)')
        else:
            cur.execute('SELECT date, description FROM events JOIN eventcodes on fk_code=pk_code WHERE date(date)=? ORDER BY datetime(date)', [date])
        return cur.fetchall()

    def get_worktime(self, date, now=None):
        cur = self.con.cursor()
        since = None
        totaltime = timedelta(0)
        for dt, e in cur.execute('SELECT date, fk_code FROM events WHERE date(date)=? ORDER BY datetime(date)', [date]):
            if since is None:
                if e == 1:
                    since = dt
                elif e == 2:
                    since = datetime.combine(date, time())
            else:
                if e == 2:
                    totaltime += dt - since
                    since = None
                elif e == 1:
                    print('Error: invalid check-in: ', dt)
        if since is not None:
            if now is None:
                totaltime += datetime.combine(date, time()) + timedelta(1) - since
            else:
                totaltime += now - since
        return totaltime

    def get_constraints(self, date=None):
        if date is None:
            return self.query_dict("SELECT * FROM workplan")
        else:
            return self.query_dict("SELECT * FROM workplan WHERE datetime(start_date) <= datetime(?) ORDER BY datetime(start_date) DESC LIMIT 1", [date])

    def save_constraint(self, constr):
        cur = self.con.cursor()
        cmd = 'REPLACE INTO workplan ({}) VALUES ({})'.format(', '.join(constr.keys()), ', '.join(['?'] * len(constr)))
        cur.execute(cmd, list(constr.values()))
        self.con.commit()

    def get_actual_weektime(self, day):
        end = day + timedelta(7)
        total = timedelta()
        while day < end:
            total += self.get_worktime(day)
            day = day + timedelta(1)
        return total

    def get_desired_weektime(self, start):
        end = start + timedelta(6)
        day = start
        c = self.get_constraints(day)
        total = c['flexible'][0]
        cur = self.con.cursor()

        while day <= end:
            d = day.weekday()
            c = self.get_constraints(day)

            total += c[WEEKDAYS[d].lower()][0]  # work time for given day

            special = cur.execute('SELECT fk_code FROM specialdays WHERE date(date)=?', [day]).fetchone()
            if special is None:
                pass
            elif special[0] == 1:  # holiday
                   total -= c[WEEKDAYS_SHORT[d].lower() + '_free'][0]
            elif special[0] == 2:  # vacation
                   total -= c[WEEKDAYS_SHORT[d].lower() + '_vacation'][0]
            elif special[0] == 3:  # sick-leave
                   total -= c[WEEKDAYS_SHORT[d].lower() + '_free'][0]

            day += timedelta(1)

        return timedelta(minutes=total)

    def get_desiredtime(self, date):
        cur = self.con.cursor()
        d = date.weekday()
        c = self.get_constraints(date)
        special = cur.execute('SELECT fk_code FROM specialdays WHERE date(date)=?', [date]).fetchone()
        if special is None:
            t = c[WEEKDAYS[d].lower()][0]
            wd = c[WEEKDAYS_SHORT[d] + '_workday'][0]
            if wd:
                t += wd * c['flexible'][0] / (c['mon_workday'][0] + c['tue_workday'][0] + c['wed_workday'][0] + c['thu_workday'][0] + c['fri_workday'][0] + c['sat_workday'][0] + c['sun_workday'][0])
            return t
        else:
            return 0

    def get_vacation(self, year):
        cur = self.con.cursor()
        cur.execute("SELECT count() FROM specialdays WHERE cast(strftime('%Y', date) as INT)=? AND fk_code=2", [year])
        return cur.fetchone()[0]

    def get_daycodes(self):
        cur = self.con.cursor()
        result = cur.execute('SELECT * FROM daycodes')
        return result.fetchall()

    def get_specialday(self, date):
        cur = self.con.cursor()
        result = cur.execute('SELECT fk_code, text FROM specialdays WHERE date(date)=date(?)', [date]).fetchone()
        return result

    def set_specialday(self, date, code, text):
        cur = self.con.cursor()
        cur.execute('REPLACE INTO specialdays (date, fk_code, text) VALUES (datetime(?), ?, ?)', [date, code, text])
        self.con.commit()

    def del_specialday(self, date):
        cur = self.con.cursor()
        cur.execute('DELETE FROM specialdays WHERE date(date)=date(?)', [date])
        self.con.commit()

    def upgrade_database(self, from_version):
        if from_version is None and self.version == '0.2':
            print('Upgrading database to {}'.format(self.version))
            cur = self.con.cursor()
            cur.execute('ALTER TABLE workplan ADD COLUMN mon_workday BOOL DEFAULT 1')
            cur.execute('ALTER TABLE workplan ADD COLUMN tue_workday BOOL DEFAULT 1')
            cur.execute('ALTER TABLE workplan ADD COLUMN wed_workday BOOL DEFAULT 1')
            cur.execute('ALTER TABLE workplan ADD COLUMN thu_workday BOOL DEFAULT 1')
            cur.execute('ALTER TABLE workplan ADD COLUMN fri_workday BOOL DEFAULT 1')
            cur.execute('ALTER TABLE workplan ADD COLUMN sat_workday BOOL DEFAULT 0')
            cur.execute('ALTER TABLE workplan ADD COLUMN sun_workday BOOL DEFAULT 0')

            cur.execute('UPDATE workplan SET mon_workday = monday > 0')
            cur.execute('UPDATE workplan SET tue_workday = tuesday > 0')
            cur.execute('UPDATE workplan SET wed_workday = wednesday > 0')
            cur.execute('UPDATE workplan SET thu_workday = thursday > 0')
            cur.execute('UPDATE workplan SET fri_workday = friday > 0')
            cur.execute('UPDATE workplan SET sat_workday = saturday > 0')
            cur.execute('UPDATE workplan SET sun_workday = sunday > 0')

            cur.execute("INSERT INTO misc VALUES ('db_version', ?)", [self.version])

            self.con.commit()
        else:
            raise NotImplementedError('Cannot upgrade database from {} to {}.'.format(from_version, self.version))




if __name__ == '__main__':
    db = Database()