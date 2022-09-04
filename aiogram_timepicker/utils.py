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


class Functions:
    create_time = None
    insert_time = None
    create_group = None
    insert_group = None
    create_cancel = None
    insert_cancel = None
    create_back = None
    insert_back = None
    create_select = None
    insert_select = None

    def __init__(self,
                 create_button, insert_button,
                 create_group, insert_group,
                 create_cancel, insert_cancel,
                 create_back, insert_back,
                 **kwargs,
                 ):
        self.create_time = Function(create_button)
        self.insert_time = Function(insert_button)
        self.create_group = Function(create_group)
        self.insert_group = Function(insert_group)
        self.create_cancel = Function(create_cancel)
        self.insert_cancel = Function(insert_cancel)
        self.create_back = Function(create_back)
        self.insert_back = Function(insert_back)
        if 'create_select' in kwargs:
            self.create_select = Function(kwargs.get('create_select'))
        if 'insert_select' in kwargs:
            self.insert_select = Function(kwargs.get('insert_select'))

    def change_actions(self, **kwargs):
        if 'create_time' in kwargs:
            self.create_time.action = kwargs.get('create_time')
        if 'insert_time' in kwargs:
            self.insert_time.action = kwargs.get('insert_time')
        if 'create_group' in kwargs:
            self.create_group.action = kwargs.get('create_group')
        if 'insert_group' in kwargs:
            self.insert_group.action = kwargs.get('insert_group')
        if 'create_cancel' in kwargs:
            self.create_cancel.action = kwargs.get('create_cancel')
        if 'insert_cancel' in kwargs:
            self.insert_cancel.action = kwargs.get('insert_cancel')
        if 'create_back' in kwargs:
            self.create_back.action = kwargs.get('create_back')
        if 'insert_back' in kwargs:
            self.insert_back.action = kwargs.get('insert_back')
        if 'create_select' in kwargs:
            self.create_select.action = Function(kwargs.get('create_select'))
        if 'insert_select' in kwargs:
            self.insert_select.action = Function(kwargs.get('insert_select'))
