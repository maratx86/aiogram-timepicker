import typing

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData
from aiogram.types import CallbackQuery

from aiogram_timepicker.result import Result, Status
from aiogram_timepicker import utils as lib_utils
from . import utils, timepicker_callback
from .utils import _default


class TimePicker:
    def __init__(self, interval: int = 1, callback: CallbackData = timepicker_callback, **kwargs):
        self.cancel = None
        if not 60 % interval:
            ValueError('MinuteTimepicker: interval must be an integer value from 0 to 59.')
        self.interval = interval
        self.callback = callback
        self.label_empty = _default['empty']
        self.label_select = _default['select']
        self.label_cancel = _default['cancel']
        self.label_back = _default['back']
        self.minute_format = _default['minute_format']
        self.minute_current_format = _default['minute_current_format']
        self.minute_unavailable_format = _default['minute_unavailable_format']
        self.str_callback = None
        self.is_available = None
        self.check_available = False
        self.group_inside_count = 10
        self.group_count = 6
        self.functions = lib_utils.Functions(
            utils.default_create_time_button,
            utils.default_insert_time_button,
            utils.default_create_group_button,
            utils.default_insert_group_button,
            utils.default_create_cancel_button,
            utils.default_insert_cancel_button,
            utils.default_create_back_button,
            utils.default_insert_back_button,
        )
        self.kwargs_params(**kwargs)

    def change_default_action(self, **kwargs):
        self.functions.change_actions(**kwargs)
        return self

    def kwargs_params(self, **kwargs):
        self.label_empty = kwargs.get('label_empty', self.label_empty or _default['empty'])
        self.label_select = kwargs.get('label_select', self.label_select or _default['select'])
        self.label_cancel = kwargs.get('label_cancel', self.label_cancel or _default['cancel'])
        self.label_back = kwargs.get('label_back', self.label_back or _default['back'])
        self.minute_format = kwargs.get('minute_format', self.minute_format or _default['minute_format'])
        self.minute_current_format = kwargs.get('minute_current_format',
                                                self.minute_current_format or _default['minute_current_format'])
        self.minute_unavailable_format = kwargs.get('minute_unavailable_format',
                                                    self.minute_unavailable_format or _default[
                                                        'minute_unavailable_format'])
        self.str_callback = kwargs.get('str_callback', self.str_callback or None)
        self.is_available = kwargs.get('is_available', self.is_available)
        self.check_available = kwargs.get('check_available', self.check_available) is True
        self.group_inside_count = kwargs.get('group_inside_count', self.group_inside_count or 10)
        self.group_count = kwargs.get('group_count', self.group_count or 6)

    async def start_picker(
            self,
            minute: int = 0,
            cancel: typing.Any = None,
            **kwargs
    ) -> InlineKeyboardMarkup:
        """
        Creates an inline keyboard with the list of minutes for selection
        :param int minute: Minute to use in the picker, if None the -1 is used. (0...59)
        :param int cancel: Action to perform after canceling, if None the keyboard is closed.
        :return: Returns InlineKeyboardMarkup object with the keyboard.
        """
        if len(kwargs):
            self.kwargs_params(**kwargs)
        self.cancel = cancel
        inline_kb = InlineKeyboardMarkup(row_width=2)
        for group_i in range(self.group_count):
            minute_from = group_i * self.group_inside_count
            minute_to = minute_from + self.group_inside_count - 1
            await self.functions.insert_group.action(
                self,
                minute_from,
                minute_to,
                inline_kb,
                await self.functions.create_group.action(self, minute, minute_from, minute_to)
            )
        await self.functions.insert_cancel.action(
            self,
            inline_kb,
            await self.functions.create_cancel.action(self)
        )
        return inline_kb

    async def time_group_picker(
            self,
            minute_curr,
            minute_from,
            minute_to,
    ):
        inline_kb = InlineKeyboardMarkup(row_width=2)
        for minute in range(minute_from, minute_to + 1, self.interval):
            await self.functions.insert_time.action(
                self,
                minute,
                inline_kb,
                await self.functions.create_time.action(self, minute_curr, minute)
            )
        await self.functions.insert_back.action(
            self,
            inline_kb,
            await self.functions.create_back.action(self)
        )
        await self.functions.insert_cancel.action(
            self,
            inline_kb,
            await self.functions.create_cancel.action(self)
        )
        return inline_kb

    async def process_group_selection(self, query: CallbackQuery, minute_data: str) -> tuple:
        group = minute_data.split('-')

        if len(group) != 3 or any(map(lambda elem: not elem.isdigit(), group)):
            await query.message.delete_reply_markup()
            return Result(
                Status.ERROR,
                message="GROUP selection numbers should be an integer"
            )
        minute_curr = int(group[0])
        minute_from = int(group[1])
        minute_to = int(group[2])
        inline_kb = await self.time_group_picker(minute_curr, minute_from, minute_to)
        await query.message.edit_reply_markup(inline_kb)

    async def process_selection(self, query: CallbackQuery, data: CallbackData) -> Result:
        """
        Process the callback_query. This method generates a new time picker if forward or
        backward is pressed. This method should be called inside a CallbackQueryHandler.
        :param query: callback_query, as provided by the CallbackQueryHandler
        :param data: callback_data, dictionary, set by `self.callback` (default timepicker_callback)
        :return: Returns an aiogram_timepicker.result.Result object.
        """
        minutes = int(data['minute']) if data['minute'].isdigit() else 0
        if data['act'] == "IGNORE":
            await query.answer(cache_time=60)
            return Result(
                Status.IGNORE,
                minutes=minutes,
            )
        if data['act'] == "CANCEL":
            if self.cancel:
                await self.cancel(query, data)
            else:
                await query.message.delete()
            return Result(
                Status.CANCELED,
                minutes=minutes,
            )
        if data['act'] == "BACK":
            await query.message.edit_reply_markup(
                await self.start_picker(
                    minutes,
                )
            )
            return Result(
                Status.BACK_TO_GROUP,
                minutes=minutes
            )
        if data['act'] == "GROUP":
            await self.process_group_selection(query, data['minute'])
            return Result(
                Status.SELECT_GROUP_MINUTE,
                minutes=int(data['minute']) if data['minute'].isdigit() else 0
            )
        if data['act'] == "SELECTED":
            return Result(
                Status.SELECTED_MINUTE,
                selected=True,
                minutes=minutes,
            )
        return Result(
            Status.UNSET,
            minutes=minutes,
        )
