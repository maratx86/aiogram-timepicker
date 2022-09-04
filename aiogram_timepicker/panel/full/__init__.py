from aiogram.utils.callback_data import CallbackData

# setting timepicker_callback prefix and parts
timepicker_callback = CallbackData('full_timepicker', 'act', 'hour', 'minute', 'second')

_default = {
    'up': '⇪',
    'down': '⇓',
    'select': 'Select',
    'cancel': 'Cancel',
    'empty': ' ',
    'hour_format': '{0:02}',
    'minute_format': '{0:02}',
    'second_format': '{0:02}',
}

from .timepicker import TimePicker
from .utils import default
