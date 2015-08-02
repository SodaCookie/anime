class Episode:
    """Episode is responsible for managing entrances and exits
    of the various collections of RubberBand objects. This object is
    NOT responsible for storing or ordering of objects. It simply finds
    differences between the states of a container between an update call
    and determines which objects should be considered entering or exiting."""

    def __init__(self, entrance=None, exit=None, demount=None, deunmount=None):
        if not entrance:
            entrance = dict()
        if not exit:
            exit = dict()
        self.entrance = entrance # Need to handle without entrance and exit
        self.exit = exit
        self.demount = demount
        self.deunmount = deunmount
        self._staged = set()
        self._mounting = set()
        self._unmounting = set()
        self._items = set()

    def render(self, iterable, surface):
        for item in iterable:
            item.render(surface)
        for item in self._unmounting:
            item.render(surface)

    def update(self, iterable, is_mounted=None, is_unmounted=None):
        """SUPER COMPLICATED WILL FIGURE OUT"""
        tmp_set = set(iterable)
        new_elements = tmp_set.difference(self._items)
        removed_elements = self._items.difference(tmp_set)
        # creating each section
        demounting_elements = self._mounting.intersection(removed_elements)
        deunmounting_elements = self._unmounting.intersection(new_elements)
        mounting_elements = new_elements.difference(deunmounting_elements)
        unmounting_elements = removed_elements.difference(demounting_elements)

        self._mounting = self._mounting | new_elements
        self._items = self._items | new_elements
        self._unmounting = self._unmounting | removed_elements # if element needs to be added
        self._staged = self._staged - removed_elements # if element was found in staged

        if self.entrance:
            for item in mounting_elements:
                dest = {key: getattr(item, key) for key in self.entrance.keys()
                    if hasattr(item, key)}
                item.force_group_set(self.entrance, True) # quietly force
                item.group_set(dest) # since if item only has key quiet can be
                                     # False (should not run error)

        if self.exit:
            for item in unmounting_elements:
                item.group_set(self.exit, True) # quietly force

        if self.entrance:
            for item in demounting_elements:
                if not self.demount:
                    item.group_set(self.entrance, True) # quietly force
                else:
                    item.group_set(self.demount, True) # quietly force

        if self.exit:
            for item in deunmounting_elements:
                if not self.deunmount:
                    item.group_set(self.exit, True) # quietly force
                else:
                    item.group_set(self.deunmount, True) # quietly force

        # This is where the items all get updated
        for item in self._items:
            item.update()

        # This is where we try to figure out which items to remove/move
        # around in each container

        # checks to see if is_mounted and is_unmounted are given
        # else defaults are used
        if not is_mounted:
            is_mounted = self.mounted
        if not is_unmounted:
            is_unmounted = self.unmounted

        # Which items were finished mounting
        mounted = set(item for item in self._mounting if is_mounted(item))
        unmounted = set(item for item in self._unmounting if is_unmounted(item))

        self._staged = self._staged | mounted # add all finished mounting items
        self._mounting = self._mounting - mounted # remove all finished mounted items
        self._items = self._items - unmounted # remove all unmounted items
        self._unmounting = self._unmounting - unmounted # remove all unmounted items


    def mounted(self, item):
        """Overrideable method in this function. Returns whether or not
        the item should be considered fully mounted"""
        if self.entrance:
            return all([not item.is_attr_dirty(key) for key in self.entrance.keys()])
        return True

    def unmounted(self, item):
        """Overrideable method in this function. Returns whether or not
        the item should be considered fully unmounted"""
        if self.exit:
            return all([not item.is_attr_dirty(key) for key in self.exit.keys()])
        return True

    def get_staged(self):
        return self._staged

    def get_mounting(self):
        return self._mounting

    def get_unmounting(self):
        return self._unmounting

    def get_items(self):
        return self._items