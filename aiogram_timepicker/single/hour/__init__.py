from aiogram.utils.callback_data import CallbackData


# setting timepicker_callback prefix and parts
timepicker_callback = CallbackData('h_tmpck', 'act', 'hour')

_default = {
    'select': 'Select',
    'cancel': 'Cancel',
    'empty': ' ',
    'hour_format': '{0:02}',
    'hour_unavailable_format': '{0:02}',
    'hour_current_format': '({0:02})',
}

from .timepicker import TimePicker
from .utils import default
