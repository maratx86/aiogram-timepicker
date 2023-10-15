from datetime import datetime, timedelta, time
from enum import Enum


class Status(Enum):
    UNSET = -1
    IGNORE = 0b100000000
    ERROR = 0b1000000000
    CANCELED = 0b00000000
    SELECTED = 0b11000111
    SELECTED_SECOND = 0b11000001
    SELECTED_MINUTE = 0b11000010
    SELECTED_HOUR = 0b11000100

    CHANGED = 0b10000111
    CHANGED_SECOND = 0b10000001
    CHANGED_MINUTE = 0b10000010
    CHANGED_HOUR = 0b10000100

    CHANGE_SECOND = 0b01000001
    CHANGE_MINUTE = 0b01000010
    CHANGE_HOUR = 0b01000100

    SELECT_GROUP_SECOND = 0b100000001
    SELECT_GROUP_MINUTE = 0b100000010
    SELECT_GROUP_HOUR = 0b100000100

    BACK_TO_GROUP = 0b100000000000000


class Result:
    selected: bool
    status: Status

    def __init__(self, status: Status = Status.UNSET, **kwargs):
        self.status = status
        self.selected = kwargs.get('selected', self.status == Status.SELECTED) is True
        self._hours = kwargs.get('hours', 0)
        self._minutes = kwargs.get('minutes', 0)
        self._seconds = kwargs.get('seconds', 0)
        self._editable = kwargs.get('editable', False) is True
        self._datetime = None
        self._timedelta = None
        self._time = None

    def _clear(self):
        self._datetime = None
        self._timedelta = None
        self._time = None

    def __str__(self):
        if self._time:
            return "Result<{status} {time}>".format(
                status=self.status,
                time=self._time.strftime("%H:%M:%S")
            )
        return "Result({status})".format(
            status=self.status,
        )

    def __repr__(self):
        return "aiogram_timepicker.result.Result(" \
               "{status}, " \
               "hours={hours}, " \
               "minutes={minutes}, " \
               "seconds={seconds}" \
               ")".format(
                status=self.status, hours=self._hours, minutes=self._minutes, seconds=self._seconds,
                )

    @property
    def editable(self):
        return self._editable

    @editable.setter
    def editable(self, value: bool):
        if not self._editable:
            raise AttributeError()
        self._editable = value is True

    @property
    def hours(self):
        return self._hours

    @hours.setter
    def hours(self, value: int):
        if not self._editable:
            raise AttributeError()
        self._hours = value
        self._clear()

    @property
    def minutes(self):
        return self._minutes

    @minutes.setter
    def minutes(self, value: int):
        if not self._editable:
            raise AttributeError()
        self._minutes = value
        self._clear()

    @property
    def seconds(self):
        return self._seconds

    @seconds.setter
    def seconds(self, value: int):
        if not self._editable:
            raise AttributeError()
        self._seconds = value
        self._clear()

    @property
    def datetime(self):
        if not self._datetime:
            self._datetime = datetime(1970, 1, 1) + self.timedelta
        return self._datetime

    @property
    def time(self):
        if not self._time:
            self._time = time(self._hours, self._minutes, self._seconds)
        return self._time

    @property
    def timedelta(self):
        if not self._timedelta:
            self._timedelta = timedelta(
                hours=self._hours,
                minutes=self._minutes,
                seconds=self._seconds
            )
        return self._timedelta
