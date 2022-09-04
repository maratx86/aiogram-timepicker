from aiogram.utils.callback_data import CallbackData


# setting timepicker_callback prefix and parts
timepicker_callback = CallbackData('c60_ts5_tmpck', 'act', 'time')

_default = {
    'select': 'Select',
    'cancel': 'Cancel',
    'empty': ' ',
    'center': '•',
    'time_format': '{0:02}',
    'time_current_format': '({0:02})',
}

from .timepicker import TimePicker
from .utils import default
