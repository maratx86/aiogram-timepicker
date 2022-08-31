from . import _default


def default(**kwargs):
    if 'label_empty' in kwargs:
        _default['empty'] = kwargs.get('label_empty')
    if 'label_select' in kwargs:
        _default['select'] = kwargs.get('label_select')
    if 'label_cancel' in kwargs:
        _default['cancel'] = kwargs.get('label_cancel')
    if 'hour_format' in kwargs:
        _default['hour_format'] = kwargs.get('hour_format')
    if 'hour_unavailable_format' in kwargs:
        _default['hour_unavailable_format'] = kwargs.get('hour_unavailable_format')
    if 'hour_current_format' in kwargs:
        _default['hour_current_format'] = kwargs.get('hour_current_format')

