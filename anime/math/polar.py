from anime.core.rubberband import RubberBand
import math

class Polar(RubberBand):

    def __init__(self, equation):
        super().__init__()
        self.phi = 0
        self.equation = equation

    def get_x(self):
        """Returns in radians"""
        return self.equation(self.phi)*math.cos(self.phi)

    def get_y(self):
        """Returns in radians"""
        return self.equation(self.phi)*math.sin(self.phi)

    def get_pos(self):
        return self.get_x(), self.get_y()
