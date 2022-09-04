import typing

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.utils.callback_data import CallbackData

from aiogram_timepicker.result import Result, Status
from aiogram_timepicker import utils as lib_utils

from . import timepicker_callback, _default, utils


class TimePicker:
    def __init__(self, interval: int = 1, callback: CallbackData = timepicker_callback, **kwargs):
        self.cancel = None
        self.interval = interval
        self.callback = callback
        self.label_empty = _default['empty']
        self.label_select = _default['select']
        self.label_cancel = _default['cancel']
        self.hour_format = _default['hour_format']
        self.hour_current_format = _default['hour_current_format']
        self.hour_unavailable_format = _default['hour_unavailable_format']
        self.str_callback = kwargs.get('str_callback', None)
        self.is_available = None
        self.check_available = False
        self.kwargs_params(**kwargs)
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

    def kwargs_params(self, **kwargs):
        self.label_empty = kwargs.get('label_empty', self.label_empty or _default['empty'])
        self.label_select = kwargs.get('label_select', self.label_select or _default['select'])
        self.label_cancel = kwargs.get('label_cancel', self.label_cancel or _default['cancel'])
        self.hour_format = kwargs.get('hour_format', self.hour_format or _default['hour_format'])
        self.hour_current_format = kwargs.get('hour_current_format', self.hour_current_format or _default['hour_current_format'])
        self.hour_unavailable_format = kwargs.get('hour_unavailable_format', self.hour_unavailable_format or _default['hour_unavailable_format'])
        self.is_available = kwargs.get('is_available', self.is_available)
        self.check_available = kwargs.get('check_available', self.check_available) is True

    async def start_picker(
        self,
        hour: int = 12,
        cancel: typing.Any = None,
        **kwargs
    ) -> InlineKeyboardMarkup:
        """
        Creates an inline keyboard with the list of hours for selection
        :param int hour: Hour to use in the picker, if None the 12 is used. (0...23)
        :param int cancel: Action to perform after canceling, if None the keyboard is closed.
        :return: Returns InlineKeyboardMarkup object with the keyboard.
        """
        if len(kwargs):
            self.kwargs_params(**kwargs)
        self.cancel = cancel
        inline_kb = InlineKeyboardMarkup(row_width=6)
        for row in range(4):
            for column in range(6):
                t = row * 6 + column
                if self.check_available and not await self.is_available(t):
                    label = self.hour_unavailable_format.format(t)
                    callback_data = self.callback.new('IGNORE', t)
                else:
                    label = self.hour_format.format(t) if t != hour else self.hour_current_format.format(t)
                    callback_data = self.callback.new('SELECTED', t) if self.callback else \
                        self.str_callback.format(hour=t)
                inline_kb.insert(InlineKeyboardButton(label, callback_data=callback_data))
            inline_kb.row()
        inline_kb.row()
        inline_kb.insert(InlineKeyboardButton(
            self.label_cancel,
            callback_data=self.callback.new('CANCEL', t) if self.callback else \
                        self.str_callback.format(hour=t),
        ))
        return inline_kb

    async def process_selection(self, query: CallbackQuery, data: CallbackData) -> Result:
        """
        Process the callback_query. This method generates a new time picker if forward or
        backward is pressed. This method should be called inside a CallbackQueryHandler.
        :param query: callback_query, as provided by the CallbackQueryHandler
        :param data: callback_data, dictionary, set by `self.callback` (default timepicker_callback)
        :return: Returns an aiogram_timepicker.result.Result object.
        """
        hours = int(data['hour']) if data['hour'] and data['hour'].isdigit() else 0
        if data['act'] == "CANCEL":
            if self.cancel:
                await self.cancel(query, data)
            else:
                await query.message.delete()
            return Result(
                Status.CANCELED,
                hours=hours
            )
        if not data['hour'].isdigit():
            return Result(Status.ERROR)
        # processing empty buttons, answering with no action
        if data['act'] == "IGNORE":
            await query.answer(cache_time=60)
            return Result(Status.IGNORE)
        if data['act'] == "SELECTED":
            return Result(
                Status.SELECTED_HOUR,
                selected=True, hours=hours,
            )
        return Result(hours=hours)
