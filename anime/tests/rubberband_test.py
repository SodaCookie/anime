import unittest

from anime.core.rubberband import RubberBand
from anime.core.filter import linear

class RubberTestClass(RubberBand):

    def __init__(self):
        super().__init__()
        self.addition = 1
        self.x = 0
        self.y = 0
        self.top_level = "test"

    def set_pos(self, pos):
        self.x = pos[0]
        self.y = pos[1]

    def get_pos(self):
        return self.x, self.y

    pos = property(get_pos, set_pos)


class RubberBandTester(unittest.TestCase):

    def setUp(self):
        self.a = RubberTestClass()
        self.b = RubberTestClass()
        self.c = RubberTestClass()
        self.b.set_owner(self.a)
        self.c.set_owner(self.b)

    def tearDown(self):
        del self.a
        del self.b
        del self.c

    def test_addition(self):
        self.assertEqual(self.c.get_absolute_value("addition"), 3)
        self.assertEqual(self.b.get_absolute_value("addition"), 2)

    def test_top_level(self):
        self.assertEqual(self.c.get_absolute_value('top_level'), "test")
        self.a.top_level = "test2"
        self.assertEqual(self.c.get_absolute_value('top_level'), "test2")
        self.b.top_level = "test3"
        self.assertEqual(self.c.get_absolute_value('top_level'), "test2")

    def test_addition_propagate(self):
        self.a.addition = 4
        self.assertEqual(self.c.get_absolute_value("addition"), 6)

    def test_no_filter(self):
        self.a.top_level = "test2"
        self.assertFalse(self.a.is_dirty()) # does not contain a filter

    def test_property(self):
        self.a.set_filter('x', linear)
        self.a.set_filter('y', linear)
        self.a.pos = (1, 2)
        self.assertEqual(self.a.get_dest('x'), 1)
        self.assertEqual(self.a.get_dest('y'), 2)

    def test_group_set(self):
        self.a.group_set(x=10, y=5, top_level="hello")
        self.assertEqual(self.a.x, 10)
        self.assertEqual(self.a.y, 5)
        self.assertEqual(self.a.top_level, "hello")

        self.a.group_set({'x' : 5, 'y' : 10, 'top_level' : "world"})
        self.assertEqual(self.a.x, 5)
        self.assertEqual(self.a.y, 10)
        self.assertEqual(self.a.top_level, "world")

    def test_group_set_error(self):
        with self.assertRaises(AttributeError):
            self.a.group_set(doesnt_exist="hello")

    def test_force_set(self):
        self.a.set_filter('x', linear, 1)
        self.b.set_filter('x', linear, 1)
        self.a.x = 10
        self.b.force_set('x', 10)
        self.assertTrue(self.a.is_attr_dirty('x'))
        self.assertEqual(self.a.x, 0)
        self.assertFalse(self.b.is_attr_dirty('x'))
        self.assertEqual(self.b.x, 10)




if __name__ == '__main__':
    unittest.main()