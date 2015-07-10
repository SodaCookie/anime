from anime.core.filter import Filter

#TODO IMPLEMENT

class FilterLine(Filter):

    def __init__(self, filters=[], done=None, speed=0):
        super().__init__(None, done, speed)
        self.filters = filters

    def __call__(self, cur, dest, speed):
        """Functions return the new value"""
        return self.call(cur, dest, speed)

    def add_filter(self, filter):
        self.filters.append(filter)

    def remove_filter(self, filter):
        self.filters.remove(filter)

    def call(self, cur, dest, speed):
        for f in self.filters:
            cur, speed = f(cur, dest, speed)
        return cur, speed

    def done(self, cur, dest, speed):
        return cur == dest

    def __getitem__(self, value):
        return FilterLine(self.filters[value], self.done, self.speed)