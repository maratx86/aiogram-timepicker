from aiogram.types import CallbackQuery
from aiogram.utils.callback_data import CallbackData

from aiogram_timepicker.panel.single.minute import timepicker
from aiogram_timepicker.result import Result, Status
from aiogram_timepicker import utils as lib_utils

from . import timepicker_callback, _default, utils


class TimePicker(timepicker.TimePicker):
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
        self.second_format = _default['second_format']
        self.second_current_format = _default['second_current_format']
        self.second_unavailable_format = _default['second_unavailable_format']
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

    def kwargs_params(self, **kwargs):
        self.label_empty = kwargs.get('label_empty', self.label_empty or _default['empty'])
        self.label_select = kwargs.get('label_select', self.label_select or _default['select'])
        self.label_cancel = kwargs.get('label_cancel', self.label_cancel or _default['cancel'])
        self.label_back = kwargs.get('label_back', self.label_back or _default['back'])
        self.second_format = kwargs.get('second_format',
                                        self.second_format or _default['second_format'])
        self.second_current_format = kwargs.get('second_current_format',
                                                self.second_current_format or _default['second_current_format'])
        self.second_unavailable_format = kwargs.get('second_unavailable_format',
                                                    self.second_unavailable_format or
                                                    _default['second_unavailable_format'])
        self.str_callback = kwargs.get('str_callback', self.str_callback or None)
        self.is_available = kwargs.get('is_available', self.is_available)
        self.check_available = kwargs.get('check_available', self.check_available) is True
        self.group_inside_count = kwargs.get('group_inside_count', self.group_inside_count or 10)
        self.group_count = kwargs.get('group_count', self.group_count or 6)

    async def process_selection(self, query: CallbackQuery, data: CallbackData) -> Result:
        """
        Process the callback_query. This method generates a new time picker if forward or
        backward is pressed. This method should be called inside a CallbackQueryHandler.
        :param query: callback_query, as provided by the CallbackQueryHandler
        :param data: callback_data, dictionary, set by `self.callback` (default timepicker_callback)
        :return: Returns an aiogram_timepicker.result.Result object.
        """
        seconds = int(data['second']) if data['second'].isdigit() else 0
        if data['act'] == "IGNORE":
            await query.answer(cache_time=60)
            return Result(
                Status.IGNORE,
                seconds=seconds,
            )
        if data['act'] == "CANCEL":
            if self.cancel:
                await self.cancel(query, data)
            else:
                await query.message.delete()
            return Result(
                Status.CANCELED,
                seconds=seconds,
            )
        if data['act'] == "BACK":
            await query.message.edit_reply_markup(
                await self.start_picker(
                    seconds,
                )
            )
            return Result(
                Status.BACK_TO_GROUP,
                seconds=seconds
            )
        if data['act'] == "GROUP":
            await self.process_group_selection(query, data['second'])
            return Result(
                Status.SELECT_GROUP_MINUTE,
                seconds=seconds
            )
        if data['act'] == "SELECTED":
            return Result(
                Status.SELECTED_SECOND,
                selected=True,
                seconds=seconds,
            )
        return Result(
            Status.UNSET,
            seconds=seconds,
        )
