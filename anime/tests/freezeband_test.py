import unittest

from anime.core.freezeband import FreezeBand
from anime.core.filter import linear

class FreezeTestClass(FreezeBand):

    def __init__(self):
        super().__init__()
        self.addition = 0
        self.x = 0
        self.y = 0
        self.top_level = "test"

    def set_pos(self, pos):
        self.x = pos[0]
        self.y = pos[1]

    def get_pos(self):
        return self.x, self.y

    pos = property(get_pos, set_pos)


class FreezeBandTester(unittest.TestCase):

    def setUp(self):
        self.a = FreezeTestClass()
        self.a.set_filter("addition", linear, 3)

    def tearDown(self):
        del self.a

    def test_freezing(self):
        self.a.addition = 10
        self.a.update()
        self.assertEqual(self.a.addition, 3)
        self.a.cancel("addition")
        self.a.update()
        self.assertEqual(self.a.addition, 3)

    def test_melting(self):
        self.a.addition = 10
        self.a.update()
        self.assertEqual(self.a.addition, 3)
        self.a.cancel("addition")
        self.a.update()
        self.a.resume("addition")
        self.a.update()
        self.assertEqual(self.a.addition, 6)

    def test_frozen(self):
        self.a.addition = 10
        self.a.cancel("addition")
        self.assertTrue(self.a.is_frozen("addition"))
        self.a.resume("addition")
        self.assertFalse(self.a.is_frozen("addition"))

    def test_hard_cancel(self):
        self.a.addition = 10
        self.a.update()
        self.a.update()
        self.assertTrue(self.a.is_attr_dirty("addition"))
        self.assertEqual(self.a.addition, 6)
        self.a.hard_cancel("addition")
        self.assertFalse(self.a.is_attr_dirty("addition"))
        self.assertEqual(self.a.addition, 6)


if __name__ == '__main__':
    unittest.main()