from anime.core.rubberband import RubberBand
from pygame import USEREVENT

COMPONENTREVENT = USEREVENT + 1

class Component(RubberBand):

    def __init__(self, pos, **kwarg):
        super().__init__()
        Anime(self, self.draw(), pos)

    def change(**kwarg):
        dict.update(self, kwarg)

    def draw(self):
        return None