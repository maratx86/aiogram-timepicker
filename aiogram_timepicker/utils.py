class Function:
    _default_action = None
    _custom_action = None

    def __init__(self, default_acton, custom_action=None):
        self._default_action = default_acton
        self._custom_action = custom_action

    @property
    def action(self):
        if self._custom_action:
            return self._custom_action
        return self._default_action

    @action.setter
    def action(self, value):
        self._custom_action = value
