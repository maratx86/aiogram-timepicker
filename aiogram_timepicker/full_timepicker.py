from datetime import datetime, timedelta
import typing

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from aiogram.types import CallbackQuery

from . import hour_picker


# setting timepicker_callback prefix and parts
timepicker_callback = CallbackData('full_timepicker', 'act', 'hour', 'minute', 'second')

_default = {
    'up': '^',
    'down': '|',
    'select': 'Select',
    'cancel': 'Cancel',
    'empty': ' ',
    'hour_format': '{0:02}',
    'minute_format': '{0:02}',
    'second_format': '{0:02}',
}


def default(**kwargs):
    if 'label_up' in kwargs:
        _default['up'] = kwargs.get('label_up')
    if 'label_down' in kwargs:
        _default['down'] = kwargs.get('label_down')
    if 'label_empty' in kwargs:
        _default['empty'] = kwargs.get('label_empty')
    if 'label_select' in kwargs:
        _default['select'] = kwargs.get('label_select')
    if 'label_cancel' in kwargs:
        _default['cancel'] = kwargs.get('label_cancel')
    if 'hour_format' in kwargs:
        _default['hour_format'] = kwargs.get('hour_format')
    if 'minute_format' in kwargs:
        _default['minute_format'] = kwargs.get('minute_format')
    if 'second_format' in kwargs:
        _default['second_format'] = kwargs.get('second_format')


class TimePicker:
    def __init__(self, interval: int = 1, callback: CallbackData = timepicker_callback, **kwargs):
        self.cancel = None
        if not 3600 % interval:
            ValueError('FullTimepicker: 3600 must be a multiple of the interval and integer value.')
        self.interval = interval
        self.callback = callback
        self.is_atomic = kwargs.get('is_atomic') is True
        self.label_up = kwargs.get('label_up', _default['up'])
        self.label_down = kwargs.get('label_down', _default['down'])
        self.label_empty = kwargs.get('label_empty', _default['empty'])
        self.label_select = kwargs.get('label_select', _default['select'])
        self.label_cancel = kwargs.get('label_cancel', _default['cancel'])
        self.hour_format = kwargs.get('hour_format', _default['hour_format'])
        self.minute_format = kwargs.get('minute_format', _default['minute_format'])
        self.second_format = kwargs.get('second_format', _default['second_format'])
        self.timezone = kwargs.get('timezone', 0)

    async def _atomic_picker(self, inline_kb: InlineKeyboardMarkup, _time: datetime):
        _tds = (
            timedelta(hours=1),
            timedelta(hours=-1),
            timedelta(minutes=1 if _time.minute + 1 < 60 else - (60 - 1)),
            timedelta(minutes=-1 if _time.minute - 1 >= 0 else 60 + -1),
            timedelta(seconds=self.interval if _time.second + self.interval < 60 else - (60 - self.interval)),
            timedelta(seconds=-self.interval if _time.second - self.interval >= 0 else 60 + -self.interval),
        )

        for _td_i in range(len(_tds)):
            _td = _tds[_td_i]
            t = _time + _td
            inline_kb.insert(InlineKeyboardButton(
                self.label_up if _td_i % 2 == 0 else self.label_down,
                callback_data=self.callback.new(
                    "CHANGE", t.strftime('%H'), t.strftime("%M"), t.strftime("%S")),
            ))
        inline_kb.row()


    async def _not_atomic_picker(self, inline_kb: InlineKeyboardMarkup, _time: datetime):
        _tds = {
            timedelta(hours=1),
            timedelta(minutes=1),
            timedelta(seconds=self.interval),
        }
        for _td in _tds:
            t = _time + _td
            inline_kb.insert(InlineKeyboardButton(
                self.label_up,
                callback_data=self.callback.new(
                    "CHANGE", t.strftime('%H'), t.strftime("%M"), t.strftime("%S")),
            ))
            t = _time - _td
            inline_kb.insert(InlineKeyboardButton(
                self.label_down,
                callback_data=self.callback.new(
                    "CHANGE", t.strftime('%H'), t.strftime("%M"), t.strftime("%S")),
            ))
        inline_kb.row()

    async def start_picker(
        self,
        hour: int = 12,
        minute: int = 00,
        second: int = 00,
        cancel: typing.Any = None,
    ) -> InlineKeyboardMarkup:
        """
        Creates an inline keyboard with the provided hour, minute and second
        :param int hour: Hour to use in the picker, if None the 12 is used. (0...23)
        :param int minute: Minute to use in the picker, if None the 00 is used. (0...59)
        :param int second: Second to use in the picker, if None the 00 is used. (0...59)
        :param int cancel: Action to perform after canceling, if None the keyboard is closed.
        :return: Returns InlineKeyboardMarkup object with the timepicker keyboard.
        """
        if hour >= 24 or hour < 0:
            ValueError('FullTimepicker: hours should be 0...23.')
        if minute >= 60 or minute < 0:
            ValueError('FullTimepicker: minutes should be 0...59.')
        if second >= 60 or second < 0:
            ValueError('FullTimepicker: seconds should be 0...59.')
        self.cancel = cancel
        inline_kb = InlineKeyboardMarkup(row_width=6)
        ignore_callback = self.callback.new("IGNORE", hour, minute, second)
        _time = datetime(1970, 1, 1, hour, minute, second)
        if self.is_atomic:
            await self._atomic_picker(inline_kb, _time)
        else:
            await self._not_atomic_picker(inline_kb, _time)
        inline_kb.insert(InlineKeyboardButton(
            self.hour_format.format(hour % 24),
            callback_data=self.callback.new('CHOOSE_H', hour, minute, second),
        ))
        inline_kb.insert(InlineKeyboardButton(
            self.minute_format.format(minute % 60),
            callback_data=self.callback.new('CHOOSE_M', hour, minute, second),
        ))
        inline_kb.insert(InlineKeyboardButton(
            self.second_format.format(second % 60),
            callback_data=self.callback.new('CHOOSE_S', hour, minute, second),
        ))
        inline_kb.row()
        inline_kb.insert(InlineKeyboardButton(
            self.label_cancel,
            callback_data=self.callback.new('CANCEL', -1, -1, -1),
        ))
        inline_kb.insert(InlineKeyboardButton(
            self.label_select,
            callback_data=self.callback.new('SELECTED', hour, minute, second),
        ))
        return inline_kb

    async def process_selection(self, query: CallbackQuery, data: CallbackData) -> tuple:
        """
        Process the callback_query. This method generates a new time picker if forward or
        backward is pressed. This method should be called inside a CallbackQueryHandler.
        :param query: callback_query, as provided by the CallbackQueryHandler
        :param data: callback_data, dictionary, set by self.callback (default timepicker_callback)
        :return: Returns a tuple (Boolean,datetime), indicating if a date is selected
                    and returning the date if so.
        """
        return_data = (False, None)
        if data['act'] == "CANCEL":
            if self.cancel:
                await self.cancel(query, data)
            else:
                await query.message.delete()
            return return_data
        hours = int(data['hour'])
        minutes = int(data['minute'])
        seconds = int(data['second'])
        time_ = datetime(1970, 1, 1, hours, minutes, seconds)
        # processing empty buttons, answering with no action
        if data['act'] == "IGNORE":
            await query.answer(cache_time=60)
        if data['act'] == "CHANGE":
            await query.message.edit_reply_markup(
                await self.start_picker(hours, minutes, seconds, cancel=self.cancel)
            )
        if data['act'] == "CHOOSE_H":
            kb = await hour_picker.HourTimePicker(1, None).start_picker(
                hours, str_callback=self.callback.new('CHANGE', '{hour}', minutes, seconds))
            await query.message.edit_reply_markup(kb)
        if data['act'] == "SELECTED":
            return_data = True, time_
        return return_data
