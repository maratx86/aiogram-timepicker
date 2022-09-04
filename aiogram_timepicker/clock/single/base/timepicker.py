from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData
from aiogram.types import CallbackQuery

from aiogram_timepicker.result import Result, Status
from aiogram_timepicker import utils as lib_utils


class TimePicker:
    functions: lib_utils.Functions

    def __init__(self, callback, **kwargs):
        self.callback = callback
        self.cancel_button_needed = kwargs.get('cancel_button_needed', True) is True
        self.select_button_needed = kwargs.get('select_button_needed', False) is True
        self._rows = 7
        self._columns = 7
        self._row_center = 3
        self._column_center = 3
        self._row_end = 6

    def kwargs_params(self, **kwargs):
        pass

    def change_default_action(self, **kwargs):
        if self.functions:
            self.functions.change_actions(**kwargs)
        return self

    async def start_picker(
            self,
            time=-1,
            **kwargs
    ) -> InlineKeyboardMarkup:
        """
        Creates an inline keyboard with the list of minutes for selection
        :param int time: Time to use in the picker, if None the -1 is used. (0...24 or -1)
        :return: Returns InlineKeyboardMarkup object with the keyboard.
        """
        if len(kwargs):
            self.kwargs_params(**kwargs)
        inline_kb = InlineKeyboardMarkup(row_width=self._rows)
        for row in range(self._rows):
            for column in range(self._columns):
                await self.functions.insert_time.action(
                    self,
                    row,
                    column,
                    inline_kb,
                    await self.functions.create_time.action(
                        self,
                        time,
                        row,
                        column,
                    ),
                )
        if self.cancel_button_needed:
            await self.functions.insert_cancel.action(
                self,
                inline_kb,
                await self.functions.create_cancel.action(self)
            )
        if self.select_button_needed:
            await self.functions.insert_select.action(
                self,
                inline_kb,
                await self.functions.create_select.action(self, time)
            )
        return inline_kb

    async def process_selection(self, query: CallbackQuery, data: CallbackData) -> Result:
        """
        Process the callback_query. This method generates a new time picker if forward or
        backward is pressed. This method should be called inside a CallbackQueryHandler.
        :param query: callback_query, as provided by the CallbackQueryHandler
        :param data: callback_data, dictionary, set by `self.callback` (default timepicker_callback)
        :return: Returns an aiogram_timepicker.result.Result object.
        """
        time = int(data['time']) if data['time'] and data['time'].isdigit() else 0

        if data['act'] == "IGNORE":
            await query.answer(cache_time=60)
            return Result(
                Status.IGNORE,
                seconds=time,
                editable=True,
            )
        if data['act'] == "CANCEL":
            return Result(
                Status.CANCELED,
                seconds=time,
                editable=True,
            )
        if data['act'] == "CHANGED":
            kb = await self.start_picker(time)
            await query.message.edit_reply_markup(kb)
            await query.answer(cache_time=60)
            return Result(
                Status.CHANGED_HOUR,
                seconds=time,
                editable=True,
            )
        if data['act'] == "SELECTED":
            return Result(
                Status.SELECTED_HOUR,
                selected=True,
                seconds=time,
                editable=True,
            )
        return Result(
            Status.UNSET,
            seconds=time,
            editable=True,
        )
