import math
from types import MethodType


def linear(cur, dest, speed):
    if cur < dest:
        if cur + speed > dest:
            return dest, speed
        return cur + speed, speed
    else:
        if cur - speed < dest:
            return dest, speed
        return cur - speed, speed


def spring(cur, dest, speed, k=0.2, b=0.5):
    # for animations, destX is really spring length (spring at rest). initial
    # position is considered as the stretched/compressed posiiton of a spring
    force = -k * (cur - dest)

    # Damping constant
    damper = -b * speed

    # usually we put mass here, but for animation purposes, specifying mass is a
    # bit redundant. you could simply adjust k and b accordingly
    # let a = (force + damper) / mass
    a = force + damper

    new_cur = cur + speed
    new_speed = speed + a

    return new_cur, new_speed


def time(cur, dest, speed, index=0, frames=10):
    #TODO
    diff = dest - cur
    return cur+diff*index/frames, diff/frames


def done_almost_equal(cur, dest, speed, ndigits=3):
    return round(cur, ndigits) == round(dest, ndigits)


def done_speed_dest(cur, dest, speed):
    return abs(speed) < 3 and abs(cur-dest) < 3


class Filter(object):
    """Takes current, destination, speed"""

    def __init__(self, call=None, done=None, speed=0):
        if call: self.call = call
        if done: self.done = done
        self.speed = speed

    def __call__(self, cur, dest, speed):
        """Functions return the new value"""
        return self.call(cur, dest, speed)

    def call(self, cur, dest, speed):
        return dest, speed

    def done(self, cur, dest, speed):
        return cur == dest


class Linear(Filter):

    def __init__(self, speed):
        super().__init__(linear, None, speed)


class Spring(Filter):

    def __init__(self, k, b):
        super().__init__(None, done_speed_dest)
        self.k = k
        self.b = b

    def call(self, cur, dest, speed):
        # for animations, destX is really spring length (spring at rest). initial
        # position is considered as the stretched/compressed posiiton of a spring
        force = -self.k * (cur - dest)

        # Damping constant
        damper = -self.b * speed

        # usually we put mass here, but for animation purposes, specifying mass is a
        # bit redundant. you could simply adjust k and b accordingly
        # let a = (force + damper) / mass
        a = force + damper

        new_cur = cur + speed
        new_speed = speed + a

        return new_cur, new_speed


class Time(Filter):
    pass