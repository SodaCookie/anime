"""Defines the FreezeBand Class"""

from anime.core.rubberband import RubberBand

class FreezeBand(RubberBand):
    """FreezeBand adds reinitializable cancels for any object"""

    FREEZE = lambda cur, dest, speed: (cur, dest)
                                               # stored internally to prevent
                                               # external mutation of freeze

    def __init__(self):
        """FreezeBand will initialize an internal dictionary _frozen_filters
        to keep track of frozen attributes"""
        super().__init__()
        object.__setattr__(self, '_frozen_filters', {})

    def cancel(self, name):
        """Will freeze the attribute name by storing the current
        filter away while replacing that filter will the class freeze
        filter. If the attribute is not dirty nothing will happen."""
        if not self.is_attr_dirty(name):
            return None
        self._frozen_filters[name] = self.get_filter(name)
        self.set_filter(name, FreezeBand.FREEZE)

    def resume(self, name):
        """Resumes a frozen object from where it was frozen,
        deleting the frozen filter. If the attribute is not frozen
        then nothing will happen."""
        frozen_filter = self._frozen_filters.get(name)
        if frozen_filter is None:
            return None
        self.set_filter(name, frozen_filter)
        del self._frozen_filters[name]

    def hard_cancel(self, name):
        """Use this instead of the RubberBand method force_set. This
        will force set the attribute to its current value as well as
        remove the frozen_filter if the attribute was frozen."""
        if self.is_frozen(name):
            self.resume(name)
        self.force_set(name, getattr(self, name))

    def is_frozen(self, name):
        """Returns if the attribute name is currently frozen"""
        return bool(self._frozen_filters.get(name))