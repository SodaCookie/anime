from functools import reduce
from types import FunctionType
from copy import deepcopy

from anime.core.filter import Filter

class RubberBand(object):

    @staticmethod
    def addition_reducer(owner, child):
        return owner + child

    @staticmethod
    def top_level_reducer(owner, child):
        return owner

    def __init__(self):
        super().__init__()

        object.__setattr__(self, "_reducers", {})
        object.__setattr__(self, "_owner", None)
        object.__setattr__(self, "_children", [])
        object.__setattr__(self, "_dirty", False)
        object.__setattr__(self, "_dirtied", set())
        object.__setattr__(self, "_filters", {})
        object.__setattr__(self, "_dest", {})

    def __setattr__(self, name, value):
        """If attribute already exists and contains a filter funtion
        than the object will be marked as dirty and the name of the attribute
        will be passed onto the _dirtied to be passed as string and the
        destination set in a dictionary"""
        if hasattr(type(self), name) and \
                isinstance(getattr(type(self), name), property):
            # Here we ignore an properties that the object may have in
            # case the user wishes to define properties
            object.__setattr__(self, name, value)
            return

        if hasattr(self, name):
            if self._filters.get(name):
                self._set_dirty(name)
                self._dest[name] = value
            else:
                # Will be clean if not filter is specified
                object.__setattr__(self, name, value)
        else:
            object.__setattr__(self, name, value)
            if isinstance(value, (int, float, complex)):
                self._reducers[name] = RubberBand.addition_reducer
            else:
                self._reducers[name] = RubberBand.top_level_reducer

    def set_owner(self, owner):
        """Used to set ownership of an object, the ownership of an object
        applies all effects down the tree additively for numeric values,
        highest level owner as boolean."""
        object.__setattr__(self, '_owner', owner)
        owner._children.append(self)

    def get_owner(self):
        return self._owner

    def get_children(self):
        return self._children

    def get_dest(self, name):
        return self._dest.get(name)

    def set_filter(self, name, filter, speed=None):
        if not hasattr(self, name):
            raise ValueError("Does not contain the attribute %s" % name)
        if isinstance(filter, FunctionType):
            if speed is None:
                speed = 0
            self._filters[name] = Filter(filter, None, speed)
        else:
            cpy_filter = deepcopy(filter)
            if speed is not None:
                cpy_filter.speed = speed
            self._filters[name] = cpy_filter

    def get_filter(self, name):
        return self._filters.get(name)

    def set_reducer(self, name, reducer):
        """Reducers are on the lowest level"""
        self._reducers[name] = reducer

    def get_speed(self, name):
        return self._filters[name].speed

    def set_speed(self, name, speed):
        self._filters[name].speed = speed

    def get_reducer(self, name):
        return self._reducers.get(name)

    def is_dirty(self):
        return self._dirty

    def get_dirtied(self):
        return self._dirtied

    def get_absolute_value(self, name):
        attr = [getattr(owner, name) for owner in self._get_owner_list()]
        if len(attr) == 1:
            return attr[0]
        return reduce(self.get_reducer(name), attr)

    def update(self):
        dirty = self._dirtied.copy()
        for name in dirty:
            value, speed = self._filters[name](getattr(self, name),
                self._dest[name], self._filters[name].speed)
            object.__setattr__(self, name, value)
            self._filters[name].speed = speed
            if self._filters[name].done(getattr(self, name),
                    self._dest[name], self._filters[name].speed):
                object.__setattr__(self, name, self._dest[name])
                self._set_clean(name)
        self._dirtied

    def _get_owner_list(self):  #FIX Should rename...
        cur = self
        owner_list = [cur]
        while cur.get_owner():
            cur = cur.get_owner()
            owner_list.append(cur)
        return owner_list[::-1]

    def _set_clean(self, name):
        self._dirtied.remove(name)
        del self._dest[name]
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