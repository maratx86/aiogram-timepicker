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
    if 'minute_format' in kwargs:
        _default['minute_format'] = kwargs.get('minute_format')
    if 'minute_unavailable_format' in kwargs:
        _default['minute_unavailable_format'] = kwargs.get('minute_unavailable_format')
    if 'minute_current_format' in kwargs:
        _default['minute_current_format'] = kwargs.get('minute_current_format')


async def default_create_time_button(timepicker, minute_curr, minute):
    label = timepicker.minute_format.format(minute) if minute_curr != minute else \
        timepicker.minute_current_format.format(minute)
    callback_data = timepicker.callback.new('SELECTED', minute)
    return InlineKeyboardButton(
        label,
        callback_data=callback_data
    )


async def default_insert_time_button(timepicker, i, inline_kb, button):
    inline_kb.insert(button)
    inline_kb.row()


async def default_create_group_button(timepicker, minute_current, minute_from, minute_to):
    label = '{0:02} - {1:02}'.format(minute_from, minute_to)
    callback_data = timepicker.callback.new('GROUP', '{0}-{1}-{2}'.format(
        minute_current, minute_from, minute_to))
    return InlineKeyboardButton(
        label,
        callback_data=callback_data
    )


async def default_insert_group_button(timepicker, minute_from, minute_to, inline_kb, button):
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
