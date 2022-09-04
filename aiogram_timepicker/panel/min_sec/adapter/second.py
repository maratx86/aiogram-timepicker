from aiogram.types import InlineKeyboardButton


def function_replace_default(callback, seconds, minutes):
    async def function_create_second_time_button(timepicker, second_curr, second):
        label = timepicker.second_format.format(second) if second_curr != second else \
            timepicker.second_current_format.format(second)
        callback_data = callback.new('CHANGE', minutes, second)
        return InlineKeyboardButton(
            label,
            callback_data=callback_data
        )

    async def function_create_second_group_button(timepicker, second_current, second_from, second_to):
        label = '{0:02} - {1:02}'.format(second_from, second_to)
        callback_data = callback.new('GRP_SEC', minutes,
                                     '{0}-{1}-{2}'.format(second_current, second_from, second_to))
        return InlineKeyboardButton(
            label,
            callback_data=callback_data
        )

    async def function_create_second_back_button(timepicker):
        callback_data = callback.new('GRP_SEC_MENU', minutes, seconds)
        return InlineKeyboardButton(
            timepicker.label_back,
            callback_data=callback_data,
        )

    async def function_create_second_cancel_button(timepicker):
        callback_data = callback.new('CHANGE', minutes, seconds)
        return InlineKeyboardButton(
            timepicker.label_cancel,
            callback_data=callback_data,
        )

    return {
        'create_time': function_create_second_time_button,
        'create_group': function_create_second_group_button,
        'create_cancel': function_create_second_cancel_button,
        'create_back': function_create_second_back_button,
    }
