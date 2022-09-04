from . import _default


def default(**kwargs):
    if 'label_up' in kwargs:
        _default['up'] = kwargs.get('label_up')
    if 'label_down' in kwargs:
        _default['down'] = kwargs.get('label_down')
    if 'label_empty' in kwargs:
        _default['empty'] = kwargs.get('label_empty')
    if 'label_select' in kwargs:
        _default['select'] = kwargs.get('label_select')
    if 'label_cancel' in kwargs:
        _default['cancel'] = kwargs.get('label_cancel')
    if 'minute_format' in kwargs:
        _default['minute_format'] = kwargs.get('minute_format')
    if 'second_format' in kwargs:
        _default['second_format'] = kwargs.get('second_format')
