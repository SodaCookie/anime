"""
This module defines the RubberBand class.
"""

from functools import reduce
from types import FunctionType, MethodType
from copy import deepcopy

from anime.core.filter import Filter
import anime.core.reducer as reducer

class RubberBand(object):
    """Core object within the anime library. It is responsible for
    assigning destinations for changes for attributes found within
    the object. This class also provides bindings to apply filters
    and reducers to the attributes to define how the attribute will
    be changed on the next update and how the absolute value of the
    attribute is given, respectively."""

    def __init__(self):
        """Rubberband takes no arguments. Initialization involves
        adding internal values that are relevant to tracking changes
        to other attributes."""
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
        destination set in a dictionary. During subclassing, in order to
        change an attribute without side effects consider using
        object.__setattr__."""
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
                self._reducers[name] = reducer.addition_reducer
            else:
                self._reducers[name] = reducer.top_level_reducer

    def set_owner(self, owner):
        """Used to set ownership of an object, the ownership of an object
        applies all effects down the tree additively for numeric values."""
        object.__setattr__(self, '_owner', owner)
        owner._children.append(self)

    def get_owner(self):
        """Returns the owner of this object if any."""
        return self._owner

    def get_children(self):
        """Returns the children of this object as a list."""
        return self._children

    def get_dest(self, name):
        """Returns the destination value of the object that attribute
        'name' is set to."""
        return self._dest.get(name)

    def set_filter(self, name, filter, speed=None, done=None):
        """'filter' can be given as a function taking cur, dest and
        speed and returning the new current and speed or a Filter
        object. If passed a function, this method will wrap the
        function within a filter object. If done is specified,
        function 'done' will wrapped with the filter function inside
        the filter object. This is not done if a Filter object is
        given. If speed is specified the speed will override the
        already given speed of a Filter object. Otherwise, the
        speed will be wrapped into Filter object with filter. Speed
        defaults to zero if not specified."""
        if not hasattr(self, name):
            raise ValueError("Does not contain the attribute %s" % name)
        if isinstance(filter, FunctionType):
            if speed is None:
                speed = 0
            self._filters[name] = Filter(filter, done, speed)
        else:
            cpy_filter = deepcopy(filter)
            if speed is not None:
                cpy_filter.speed = speed
            self._filters[name] = cpy_filter

    def get_filter(self, name):
        """Returns the filter associated to the given attribute."""
        return self._filters.get(name)

    def remove_filter(self, name):
        """Removed the filter attached to the given name. If that
        attribute currently had a destination, than the attribute
        will be set to that destination and marked clean."""
        if self._dest.get(name):
            object.__setattr__(self, name, self._dest[name])
            self._set_clean(name)
        del self._filters[name]

    def set_reducer(self, name, reducer):
        """Attach a reducer to the attribute with the given name."""
        self._reducers[name] = reducer

    def force_set(self, name, value):
        """Force set will override any filters present on the attribute
        and if the attribute already has a destination that attribute
        will be cleaned and set to the forced value."""
        object.__setattr__(self, name, value)
        if self.is_attr_dirty(name):
            self._set_clean(name)

    def group_set(self, _setter=None, _quiet=False, **kwarg):
        """Group set is a method used to apply changes to multiple
        existing attributes on a RubberBand object with one call.
        This method can take a dictionary and/or take keyword arguments,
        where each key is the name of the attribute and the value is the
        value of that attribute. Keyword arguments will override the values
        found in the passed dictionary if one is provided. If a key that
        is passed is not an attribute of the object than an AttributeError
        is raised. If _quiet is True then no Exception will be raised
        do to certain implementations"""
        if not _setter:
            _setter = {}
        _setter.update(kwarg)

        for key, value in _setter.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                if not _quiet:
                    raise AttributeError("Object has no attribute '%s'"%key)

    def force_group_set(self, _setter=None, _quiet=False, **kwarg):
        """Acts exactly like group_set but when setting an attribute force_set
        is called instead of setattr."""
        if not _setter:
            _setter = {}
        _setter.update(kwarg)

        for key, value in _setter.items():
            if hasattr(self, key):
                self.force_set(key, value)
            else:
                if not _quiet:
                    raise AttributeError("Object has no attribute '%s'"%key)

    def get_speed(self, name):
        """Returns the current speed attached the name's filter."""
        return self._filters[name].speed

    def set_speed(self, name, speed):
        """Override the set of the name's given filter"""
        self._filters[name].speed = speed

    def get_reducer(self, name):
        """Returns the reducer of the given attribute name"""
        return self._reducers.get(name)

    def is_dirty(self):
        """Returns True if any attributes of the object are currently not
        at their destination."""
        return self._dirty

    def is_attr_dirty(self, name):
        return name in self.get_dirtied()

    def get_dirtied(self):
        """Returns the list of attributes that have not reached their
        destination."""
        return self._dirtied

    def get_absolute_value(self, name):
        """Returns the absolute value of the attribute name after
        being passed through its given reducer. The reducer used will
        be the objects own reducer."""
        attr = [getattr(owner, name) for owner in self._get_owner_list()]
        if len(attr) == 1:
            return attr[0]
        return reduce(self.get_reducer(name), attr)

    def update(self):
        """Passes all dirtied attributes through their respective filters.
        If any attributes have reached their destination then that
        attribute will be set as clean."""
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

    def _get_owner_list(self):
        """returns the owner hierarchy above the object. Top owner
        is always first index. The object itself is always the last
        index."""
        cur = self
        owner_list = [cur]
        while cur.get_owner():
            cur = cur.get_owner()
            owner_list.append(cur)
        return owner_list[::-1]

    def _set_clean(self, name):
        """Removes the name from the list of dirtied attributes,
        deletes the destination and checks if entire object is
        clean."""
        self._dirtied.remove(name)
        del self._dest[name]
        if not self._dirtied:
            object.__setattr__(self, "_dirty", False)

    def _set_dirty(self, name):
        """Sets attribute name as dirty and added to _dirtied."""
        self._dirtied.add(name)
        object.__setattr__(self, "_dirty", True)