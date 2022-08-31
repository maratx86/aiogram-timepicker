from aiogram.types import InlineKeyboardButton

from . import _default


def default(**kwargs):
    if 'label_empty' in kwargs:
        _default['empty'] = kwargs.get('label_empty')
    if 'label_select' in kwargs:
        _default['select'] = kwargs.get('label_select')
    if 'label_cancel' in kwargs:
        _default['cancel'] = kwargs.get('label_cancel')
    if 'label_back' in kwargs:
        _default['back'] = kwargs.get('label_back')
    if 'second_format' in kwargs:
        _default['second_format'] = kwargs.get('second_format')
    if 'minute_unavailable_format' in kwargs:
        _default['second_unavailable_format'] = kwargs.get('second_unavailable_format')
    if 'second_current_format' in kwargs:
        _default['second_current_format'] = kwargs.get('second_current_format')


async def default_create_time_button(timepicker, second_curr, second):
    label = timepicker.second_format.format(second) if second_curr != second else \
        timepicker.second_current_format.format(second)
    callback_data = timepicker.callback.new('SELECTED', second)
    return InlineKeyboardButton(
        label,
        callback_data=callback_data
    )


async def default_insert_time_button(timepicker, i, inline_kb, button):
    inline_kb.insert(button)
    inline_kb.row()


async def default_create_group_button(timepicker, second_current, second_from, second_to):
    label = '{0:02} - {1:02}'.format(second_from, second_to)
    callback_data = timepicker.callback.new('GROUP', '{0}-{1}-{2}'.format(
        second_current, second_from, second_to))
    return InlineKeyboardButton(
        label,
        callback_data=callback_data
    )


async def default_insert_group_button(timepicker, second_from, second_to, inline_kb, button):
    inline_kb.insert(button)
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
