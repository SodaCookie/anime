import unittest

import pygame

from anime.core.anime import Anime

class AnimeTester(unittest.TestCase):

    def setUp(self):
        pygame.display.init()
        self.anime = Anime((0, 0), (1, 1))

    def tearDown(self):
        pygame.display.quit()
        del self.anime

    def test_dirty(self):
        self.anime
        self.assertTrue()