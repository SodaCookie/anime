class _RubberBand(object):

    def __init__(self):
        super().__init__()

        self._owner = None
        self._children = []
        self._dirty = False
        self._dirtied = set()
        self._filters = {}
        self._reducers = {}
        self._dest = {}

    def __setattr__(self, name, value):
        """If attribute already exists and contains a filter funtion
        than the object will be marked as dirty and the name of the attribute
        will be passed onto the _dirtied to be passed as string and the
        destination set in a dictionary"""
        if hasattr(self, name) and self._filters.get(name):
            self._set_dirty(name)
            self._dest[name] = value
        else:
            object.__setattr__(self, name, value)

    def set_owner(self, owner):
        """Used to set ownership of an object, the ownership of an object
        applies all effects down the tree additively for numeric values,
        highest level owner as boolean."""
        object.__setattr__('owner', owner)
        owner._children.append(self)

    def get_owner(self):
        return self._owner

    def get_dest(self, name):
        return self._dest.get(name)

    def set_filter(self, name, filter):
        self._filters[name] = filter

    def get_filter(self, name):
        return self._filters.get(name)

    def set_reducer(self, name, reducer):
        self._reducers[name] = reducer

    def get_reducer(self, name):
        return self._reducers.get(name)

    def is_dirty(self):
        return self._dirty

    def get_absolute_value(self, name):
        if self.get_owner():

    def _update(self):
        for name in self._dirtied:
            if not self._filters.get(name):
                object.__setattr__(self, name, self._dest[name])
            else:
                object.__setattr__(self, name,
                    self._filters[name](getattr(self, name), self._dest[name]))
            if self._filters.done(getattr(self, name), self._dest[name]):
                self._set_clean(name)

    def _get_top_reducer(self, name):
        if self.get_owner():
            return self.get_owner().get_reducer()
        return self._reducers

    def _set_clean(self, name):
        self._dirtied.remove(name)
        if not self._dirtied:
            object.__setattr__(self, "_dirty", False)

    def _set_dirty(self, name):
        self._dirtied.add(name)
        object.__setattr__(self, "_dirty", True)

        # self.surface = surface
        # self.pos = pos
        # self.visible = False
        # self.opacity = 255
        # self.angle = 0
        # self.width = surface.get_width()
        # self.height = surface.get_height()