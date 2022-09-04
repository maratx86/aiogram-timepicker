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
        if column == 3:
            return True, 0
        elif column == 2:
            return True, 57
        elif column == 4:
            return True, 3
        return False, None
    if row == 8:
        if column == 3:
            return True, 30
        elif column == 2:
            return True, 33
        elif column == 4:
            return True, 27
        return False, None
    if row == 1:
        if column == 1:
            return True, 54
        if column == 5:
            return True, 6
        return False, None
    if row == 2:
        if column == 0:
            return True, 51
        if column == 6:
            return True, 9
        return False, None
    if row == 3:
        if column == 0:
            return True, 48
        if column == 6:
            return True, 12
        return False, None
    if row == 4:
        if column == 0:
            return True, 45
        if column == 6:
            return True, 15
        return False, None
    if row == 5:
        if column == 0:
            return True, 42
        if column == 6:
            return True, 18
        return False, None
    if row == 6:
        if column == 0:
            return True, 39
        if column == 6:
            return True, 21
        return False, None
    if row == 7:
        if column == 1:
            return True, 36
        if column == 5:
            return True, 24
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
        if row == timepicker._row_center and column == timepicker._column_center:
            label = timepicker.label_center
        else:
            label = timepicker.label_empty
        callback_data = timepicker.callback.new('IGNORE', row * timepicker._rows + column)
    return InlineKeyboardButton(
        label,
        callback_data=callback_data
    )


async def default_insert_time_button(timepicker, row, column, inline_kb, button):
    inline_kb.insert(button)
    if column >= timepicker._row_end:
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
