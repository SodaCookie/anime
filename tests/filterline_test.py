import unittest

from anime.core.rubberband import RubberBand
from anime.core.filter import *
from anime.core.filterline import FilterLine

class RubberTestClass(RubberBand):

    def __init__(self):
        super().__init__()
        self.linear = 0
        self.spring = 0


class FilterTester(unittest.TestCase):

    def setUp(self):
        self.a = RubberTestClass()
        self.line = FilterLine()

    def tearDown(self):
        del self.a




if __name__ == '__main__':
    unittest.main()