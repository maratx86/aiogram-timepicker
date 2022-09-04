from aiogram.types import CallbackQuery
from aiogram.utils.callback_data import CallbackData


from aiogram_timepicker import utils as lib_utils
from aiogram_timepicker.result import Result

from ..base import BaseTimePicker
from . import timepicker_callback, _default, utils


class TimePicker(BaseTimePicker):
    def __init__(self, callback: CallbackData = timepicker_callback, **kwargs):
        super().__init__(callback, **kwargs)
        self._rows = 9
        self._row_center = 4
        self.label_empty = _default['empty']
        self.label_center = _default['center']
        self.label_select = _default['select']
        self.label_cancel = _default['cancel']
        self.time_format = _default['time_format']
        self.time_current_format = _default['time_current_format']
        self.functions = lib_utils.Functions(
            utils.default_create_time_button,
            utils.default_insert_time_button,
            None,
            None,
            utils.default_create_cancel_button,
            utils.default_insert_cancel_button,
            utils.default_create_back_button,
            utils.default_insert_back_button,
            create_select=utils.default_create_select_button,
            insert_select=utils.default_insert_select_button,
        )
        self.kwargs_params(**kwargs)

    def kwargs_params(self, **kwargs):
        self.label_empty = kwargs.get('label_empty', self.label_empty or _default['empty'])
        self.label_select = kwargs.get('label_select', self.label_select or _default['select'])
        self.label_cancel = kwargs.get('label_cancel', self.label_cancel or _default['cancel'])
        if 'time_format' in kwargs:
            self.time_format = kwargs.get('time_format') or _default.get('time_format')
        if 'time_current_format' in kwargs:
            self.time_current_format = kwargs.get('time_current_format') or _default.get('time_current_format')

    async def process_selection(self, query: CallbackQuery, data: CallbackData) -> Result:
        """
        Process the callback_query. This method generates a new time picker if forward or
        backward is pressed. This method should be called inside a CallbackQueryHandler.
        :param query: callback_query, as provided by the CallbackQueryHandler
        :param data: callback_data, dictionary, set by `self.callback` (default timepicker_callback)
        :return: Returns an aiogram_timepicker.result.Result object.
        """
        r = await super().process_selection(query, data)
        r.minutes = r.seconds
        r.seconds = 0
        r.editable = False
        return r
