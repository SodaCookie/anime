import unittest

from anime.core.rubberband import RubberBand
import anime.core.filter as filter
from anime.core.pipe import Pipe

class RubberTestClass(RubberBand):

    def __init__(self):
        super().__init__()
        self.addition = 1
        self.x = 0
        self.y = 0
        self.top_level = "test"


class PipeTester(unittest.TestCase):

    def setUp(self):
        self.a = RubberTestClass()
        self.pipe = Pipe([filter.Linear(-2), filter.linear, filter.Linear(3)], lambda cur, dest, speed: cur==3)

    def tearDown(self):
        del self.a
        del self.pipe

    def test_pipe(self):
        self.a.set_filter("addition", self.pipe)
        self.a.addition = 4
        self.a.update()
        self.assertEqual(self.a.addition, 2)

    def test_done_condition(self):
        self.a.set_filter("addition", self.pipe)
        self.a.addition = 4
        self.a.update()
        self.assertTrue(self.a.is_dirty())
        self.a.update()
        self.assertFalse(self.a.is_dirty())
        self.assertEqual(self.a.addition, 4)

    def test_slicing(self):
        self.a.set_filter("addition", self.pipe[1:])
        self.a.addition = 10
        self.a.update()
        self.assertEqual(self.a.addition, 4)


if __name__ == '__main__':
    unittest.main()