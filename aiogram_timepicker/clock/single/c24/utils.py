from aiogram.types import InlineKeyboardButton

from . import _default


def default(**kwargs):
    if 'label_empty' in kwargs:
        _default['empty'] = kwargs.get('label_empty')
    if 'label_center' in kwargs:
        _default['center'] = kwargs.get('label_center')
    if 'label_select' in kwargs:
        _default['select'] = kwargs.get('label_select')
    if 'label_cancel' in kwargs:
        _default['cancel'] = kwargs.get('label_cancel')
    if 'time_format' in kwargs:
        _default['time_format'] = kwargs.get('time_format')
    if 'time_current_format' in kwargs:
        _default['time_current_format'] = kwargs.get('time_current_format')


def _time_button_or_not(row, column):
    if row == 0:
        if column == 1:
            return True, 22
        elif column == 2:
            return True, 23
        elif column == 3:
            return True, 0
        elif column == 4:
            return True, 1
        elif column == 5:
            return True, 2
    elif row == 1:
        if column == 0:
            return True, 20
        elif column == 1:
            return True, 21
        elif column == 5:
            return True, 3
        elif column == 6:
            return True, 4
    elif row == 5:
        if column == 0:
            return True, 16
        elif column == 1:
            return True, 15
        elif column == 5:
            return True, 9
        elif column == 6:
            return True, 8
    elif row == 6:
        if column == 1:
            return True, 14
        elif column == 2:
            return True, 13
        elif column == 3:
            return True, 12
        elif column == 4:
            return True, 11
        elif column == 5:
            return True, 10
    elif row == 2:
        if column == 0:
            return True, 19
        elif column == 6:
            return True, 5
    elif row == 3:
        if column == 0:
            return True, 18
        elif column == 6:
            return True, 6
    elif row == 4:
        if column == 0:
            return True, 17
        elif column == 6:
            return True, 7
    return False, None


async def default_create_time_button(timepicker, time_curr, row, column):
    t_b, t = _time_button_or_not(row, column)
    if t_b:
        label = timepicker.time_format.format(t) if time_curr != t else \
            timepicker.time_current_format.format(t)
        if timepicker.select_button_needed:
            callback_data = timepicker.callback.new('CHANGED', t)
        else:
            callback_data = timepicker.callback.new('SELECTED', t)
    else:
        if row == column == 3:
            label = timepicker.label_center
        else:
            label = timepicker.label_empty
        callback_data = timepicker.callback.new('IGNORE', row * 7 + column)
    return InlineKeyboardButton(
        label,
        callback_data=callback_data
    )


async def default_insert_time_button(timepicker, row, column, inline_kb, button):
    inline_kb.insert(button)
    if column >= 6:
        inline_kb.row()


async def default_create_back_button(timepicker):
    callback_data = timepicker.callback.new('BACK', 0)
    return InlineKeyboardButton(
        timepicker.label_back,
        callback_data=callback_data,
    )


async def default_insert_back_button(timepicker, inline_kb, button):
    inline_kb.insert(button)


async def default_create_cancel_button(timepicker):
    callback_data = timepicker.callback.new('CANCEL', 0)
    return InlineKeyboardButton(
        timepicker.label_cancel,
        callback_data=callback_data,
    )


async def default_insert_cancel_button(timepicker, inline_kb, button):
    inline_kb.insert(button)


async def default_create_select_button(timepicker, time):
    callback_data = timepicker.callback.new('SELECTED', time)
    return InlineKeyboardButton(
        timepicker.label_select,
        callback_data=callback_data,
    )


async def default_insert_select_button(timepicker, inline_kb, button):
    inline_kb.insert(button)
