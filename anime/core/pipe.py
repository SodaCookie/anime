"""Defines the Pipe Object"""

from anime.core.filter import Filter
from types import FunctionType

class Pipe(Filter):
    """Class designed to combine several filters together at once.
    The done condition is held by the Pipe filter and will override
    any of its children's done conditions. It is also possible to
    slice the object into another filter."""

    def __init__(self, filters, done):
        """Takes filters, will convert all the filters into Filter
        object, if a FunctionType is given it'll be converted into
        a Filter object. The done argument defined the done condition
        which is the overriding condition for the object to stop.
        The done condition does not have access to speed which will
        be given as 0."""
        super().__init__(None, done, 0)
        self.filters = []
        for filter in filters:
            if isinstance(filter, FunctionType):
                self.filters.append(Filter(filter, None, 0))
            elif isinstance(filter, Filter):
                self.filters.append(filter)
            else:
                raise ValueError("One or more filters were not a Filter or FunctionType")

    def call(self, cur, dest, speed):
        """Override the call function"""
        for filter in self.filters:
            cur, filter.speed = filter(cur, dest, filter.speed)
        return cur, speed

    def __getitem__(self, value):
        """Returns another Pipe object with filters from each slice.
        The done condition remains the same."""
        return Pipe(self.filters[value], self.done)