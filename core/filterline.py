from anime.core.filter import Filter

#TODO IMPLEMENT

class FilterLine(list):

    def __init__(self, filters=[], speed=0):
        super().__init__(filters)
        self.speed=0

    def __call__(self, cur, dest, speed):
        """Functions return the new value"""
        return self.call(cur, dest, speed)

    def add_filter(self, filter):
        self.filters.append(filter)

    def call(self, cur, dest, speed):
        for f in self.filters:
            cur, speed = f(cur, dest, speed)
        return cur, speed

    def done(self, cur, dest, speed):
        return cur == dest