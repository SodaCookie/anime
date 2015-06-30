from collections import OrderedDict

from anime.core.rubberband import RubberBand
import anime.core.renderer as renderer

class Anime(RubberBand):

    def __init__(self, surface, x, y):
        super().__init__()
        object.__setattr__(self, "_renderers", OrderedDict())

        self.surface = surface
        self.x = x
        self.y = y
        self.angle = 0
        self.set_renderer('angle', renderer.angle_renderer)
        self.w_ratio = 1
        self.h_ratio = 1
        self.opacity = 255

    def set_renderer(self, name, renderer):
        self._renderers[name] = renderer

    def get_renderer(self, name):
        return self._renderers.get(name)

    def render(self, surface, offset=(0, 0)):
        tmp_surf = self.surface.copy()
        prev_w, prev_h = tmp_surf.get_size()

        for name, renderer in self._renderers.items():
            tmp_surf = renderer(tmp_surf, self.get_absolute_value(name))

        new_w, new_h = tmp_surf.get_size()
        offsetx, offsety = (new_w - prev_w) // 2, (new_h - prev_h) // 2

        for child in self.get_children():
            child.render(tmp_surf, (offsetx, offsety))

        surface.blit(tmp_surf,
            (self.x-new_w//2+offset[0], self.y-new_h//2+offset[1]))