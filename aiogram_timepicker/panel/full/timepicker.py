from datetime import datetime, timedelta
import typing

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from aiogram.types import CallbackQuery

from aiogram_timepicker import result
from aiogram_timepicker.panel.single import minute, second, hour
from . import _default, timepicker_callback, adapter


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

    async def _process_selection_all_int(self, query: CallbackQuery, act: str, seconds: int, minutes: int, hours: int):
        if act == "CHANGE":
            await query.message.edit_reply_markup(
                await self.start_picker(hours, minutes, seconds, cancel=self.cancel)
            )
            return result.Result(
                result.Status.CHANGED,
                hours=hours, minutes=minutes, seconds=seconds,
            )
        elif act == "SELECTED":
            return result.Result(
                result.Status.SELECTED,
                hours=hours, minutes=minutes, seconds=seconds,
            )
        elif act == "CHOOSE_H":
            kb = await hour.TimePicker(
                1, None,
                str_callback=self.callback.new('CHANGE', '{hour}', minutes, seconds))\
                .start_picker(hours)
            await query.message.edit_reply_markup(kb)
            return result.Result(
                result.Status.CHANGE_HOUR,
                hours=hours, minutes=minutes, seconds=seconds,
            )
        elif act == "CHOOSE_M" or act == "GRP_MIN_MENU":
            kb = await minute.TimePicker(self.interval // 60 if self.interval >= 60 else 1, self.callback)\
                .change_default_action(
                **adapter.minute.function_replace_default(
                    self.callback, seconds, minutes, hours)
            ).start_picker(minutes)
            await query.message.edit_reply_markup(kb)
            return result.Result(
                result.Status.CHANGE_MINUTE,
                hours=hours, minutes=minutes, seconds=seconds,
            )
        elif act == "CHOOSE_S" or act == "GRP_SEC_MENU":
            kb = await second.TimePicker(self.interval, None)\
                .change_default_action(
                **adapter.second.function_replace_default(
                    self.callback, seconds, minutes, hours)
            ).start_picker(seconds)
            await query.message.edit_reply_markup(kb)
            return result.Result(
                result.Status.CHANGE_SECOND,
                hours=hours, minutes=minutes, seconds=seconds,
            )
        return result.Result()

    async def _process_selection_not_int(self, query: CallbackQuery, act: str, seconds: str, minutes: str, hours: str):
        # processing empty buttons, answering with no action
        if act == "GRP_MIN":
            m = minutes.split('-')[0]
            m = int(m) if m.isdigit() else 0
            await minute.TimePicker(
                self.interval // 60 if self.interval >= 60 else 1, self.callback
            ).change_default_action(
                **adapter.minute.function_replace_default(
                    self.callback, seconds, m, hours)
            ).process_group_selection(query, minutes)
            return result.Result(
                result.Status.SELECT_GROUP_MINUTE,
                **{
                    hours: int(hours) if hours.isdigit() else 0,
                    seconds: int(seconds) if seconds.isdigit() else 0,
                }
            )
        elif act == "GRP_SEC":
            s = seconds.split('-')[0]
            s = int(s) if s.isdigit() else 0
            await second.TimePicker(self.interval, self.callback).change_default_action(
                **adapter.second.function_replace_default(
                    self.callback, s, minutes, hours)
            ).process_group_selection(query, seconds)
            return result.Result(
                result.Status.SELECT_GROUP_SECOND,
                **{
                    hours: int(hours) if hours.isdigit() else 0,
                    minutes: int(minutes) if minutes.isdigit() else 0,
                }
            )
        return result.Result()

    async def process_selection(self, query: CallbackQuery, data: CallbackData) -> result.Result:
        """
        Process the callback_query. This method generates a new time picker if forward or
        backward is pressed. This method should be called inside a CallbackQueryHandler.
        :param query: callback_query, as provided by the CallbackQueryHandler
        :param data: callback_data, dictionary, set by `self.callback` (default timepicker_callback)
        :return: Returns an aiogram_timepicker.result.Result object.
        """
        if data['act'] == "CANCEL":
            if self.cancel:
                await self.cancel(query, data)
            else:
                await query.message.delete()
            return result.Result(result.Status.CANCELED)
        elif data['act'] == "IGNORE":
            await query.answer(cache_time=60)
            return result.Result()
        if not (data['hour'].isdigit() and data['minute'].isdigit() and data['second'].isdigit()):
            return await self._process_selection_not_int(
                query, data['act'], data['second'], data['minute'], data['hour']
            )
        return await self._process_selection_all_int(
            query, data['act'], int(data['second']), int(data['minute']), int(data['hour'])
        )
