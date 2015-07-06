from anime.core.anime import Anime

class Component(Anime):

    def __init__(self, **kwarg):
        dict.__init__(self, **kwarg)
        Anime(self, self.render(), pass)

    def change(**kwarg):
        dict.update(self, kwarg)

    def render(self):
        return None