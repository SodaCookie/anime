from anime.core.rubberband import RubberBand

class QuadraticBezier(RubberBand):

    def __init__(self, path):
        """QuadraticBezier takes a path of a list of 3 pairs of
        coordinates. Because QuadraticBezier extends Rubberband,
        it is possible to place filters on t and path. Usage of
        this is class is to convert the parametric function for
        Bezier curves into appropriate x and y values for animation"""
        super().__init__()
        self.t = 0
        self.path = path

    def get_x(self):
        return (1-self.t)**2*self.path[0][0] + \
            2*(1-self.t)*self.t*self.path[1][0] + \
            self.t**2*self.path[2][0]

    def get_y(self):
        return (1-self.t)**2*self.path[0][1] + \
            2*(1-self.t)*self.t*self.path[1][1] + \
            self.t**2*self.path[2][1]

    def get_pos(self):
        return self.get_x(), self.get_y()


class CubicBezier(RubberBand):

    def __init__(self, path):
        """CubicBezier takes a path of a list of 4 pairs of
        coordinates. Because CubicBezier extends Rubberband,
        it is possible to place filters on t and path. Usage of
        this is class is to convert the paramet ric function for
        Bezier curves into appropriate x and y values for animation"""
        super().__init__()
        self.t = 0
        self.path = path

    def get_x(self):
        return (1-self.t)**3*self.path[0][0] + \
            3*(1-self.t)**2*self.t*self.path[1][0] + \
            3*(1-self.t)*self.t**2*self.path[2][0] + \
            self.t**3*self.path[3][0]

    def get_y(self):
        return (1-self.t)**3*self.path[0][1] + \
            3*(1-self.t)**2*self.t*self.path[1][1] + \
            3*(1-self.t)*self.t**2*self.path[2][1] + \
            self.t**3*self.path[3][1]

    def get_pos(self):
        return self.get_x(), self.get_y()
