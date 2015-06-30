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


def spring(cur, dest, speed):
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

def done_speed_dest(cur, dest, speed):
    return speed == 0 and cur == dest


class Filter(object):
    """Takes current, destination, speed"""

    def __init__(self, call=None, done=None):
        if call: self.call = call
        if done: self.done = done

    def __call__(self, cur, dest, speed):
        """Functions return the new value"""
        return self.call(cur, dest, speed)

    def call(self, cur, dest, speed):
        return dest, speed

    def done(self, cur, dest, speed):
        return cur == dest


LINEAR = Filter(linear)
SPRING = Filter(spring, done_speed_dest)