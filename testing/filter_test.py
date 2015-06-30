import unittest

from anime.core.rubberband import RubberBand
from anime.core.filter import *

class RubberTestClass(RubberBand):

    def __init__(self):
        super().__init__()
        self.linear = 0
        self.spring = 0


class FilterTester(unittest.TestCase):

    def setUp(self):
        self.a = RubberTestClass()
        self.a.set_filter('linear', LINEAR, 3)
        self.a.set_filter('spring', SPRING)

    def tearDown(self):
        del self.a

    def test_dirty(self):
        self.a.linear = 1
        self.assertTrue(self.a.is_dirty())

    def test_clean(self):
        self.a.linear = 1
        self.assertTrue(self.a.is_dirty())
        self.a.update()
        self.assertFalse(self.a.is_dirty())


if __name__ == '__main__':
    unittest.main()