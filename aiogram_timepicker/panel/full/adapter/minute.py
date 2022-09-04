from aiogram.types import InlineKeyboardButton


def function_replace_default(callback, seconds, minutes, hours):
    async def function_create_minute_time_button(timepicker, minute_curr, minute):
        label = timepicker.minute_format.format(minute) if minute_curr != minute else \
            timepicker.minute_current_format.format(minute)
        callback_data = callback.new('CHANGE', hours, minute, seconds)
        return InlineKeyboardButton(
            label,
            callback_data=callback_data
        )

    async def function_create_minute_group_button(timepicker, minute_current, minute_from, minute_to):
        label = '{0:02} - {1:02}'.format(minute_from, minute_to)
        callback_data = callback.new('GRP_MIN', hours, '{0}-{1}-{2}'.format(
            minute_current, minute_from, minute_to), seconds)
        return InlineKeyboardButton(
            label,
            callback_data=callback_data
        )

    async def function_create_minute_back_button(timepicker):
        callback_data = callback.new('GRP_MIN_MENU', hours, 0, seconds)
        return InlineKeyboardButton(
            timepicker.label_back,
            callback_data=callback_data,
        )

    async def function_create_minute_cancel_button(timepicker):
        callback_data = callback.new('CHANGE', hours, minutes, seconds)
        return InlineKeyboardButton(
            timepicker.label_cancel,
            callback_data=callback_data,
        )

    return {
        'create_time': function_create_minute_time_button,
        'create_group': function_create_minute_group_button,
        'create_cancel': function_create_minute_cancel_button,
        'create_back': function_create_minute_back_button,
    }
