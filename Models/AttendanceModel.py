class Attendance:
    def __init__(self, student_id, date, time_in, time_out, status, hours_worked):
        self._student_id = student_id
        self._date = date
        self._time_in = time_in
        self._time_out = time_out
        self._status = status
        self._hours_worked = hours_worked

    @property
    def student_id(self):
        return self._student_id

    @student_id.setter
    def student_id(self, student_id):
        self._student_id = student_id

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, date):
        self._date = date

    @property
    def time_in(self):
        return self._time_in

    @time_in.setter
    def time_in(self, time_in):
        self._time_in = time_in

    @property
    def time_out(self):
        return self._time_out

    @time_out.setter
    def time_out(self, time_out):
        self._time_out = time_out

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status):
        self._status = status

    @property
    def hours_worked(self):
        return self._hours_worked

    @hours_worked.setter
    def hours_worked(self, hours):
        self._hours_worked = hours
