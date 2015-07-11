from anime.core.rubberband import RubberBand

class Parametric(RubberBand):

    def __init__(self, equations):
        super().__init__()
        self.t = 0
        self.equations = equations

    def get(self, attribute):
        return self.equations[attribute](self.t)


class Parametric2D(RubberBand):

    def __init__(self, xequation, yequation):
        super().__init__()
        self.t = 0
        self.xequation = xequation
        self.yequation = yequation

    def get_x(self):
        return self.xequation(self.t)

    def get_y(self):
        return self.yequation(self.t)

    def get_pos(self):
        return self.get_x(), self.get_y()
