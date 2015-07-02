from collections import OrderedDict

from pygame import Surface

from anime.core.rubberband import RubberBand
import anime.core.renderer as renderer
import anime.core.reducer as reducer

class Anime(RubberBand):

    def __init__(self, surface, x, y):
        super().__init__()
        object.__setattr__(self, "_renderers", OrderedDict())

        assert isinstance(surface, Surface), "surface must be of type Surface"

        self.surface = surface
        self.x = x
        self.y = y
        self.w_ratio = 1
        self.set_renderer('w_ratio', renderer.wratio_renderer)
        self.set_reducer('w_ratio', reducer.mult_reducer)
        self.h_ratio = 1
        self.set_renderer('h_ratio', renderer.hratio_renderer)
        self.set_reducer('h_ratio', reducer.mult_reducer)
        self.angle = 0
        self.set_renderer('angle', renderer.angle_renderer)
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
            (round(self.x)-new_w//2+offset[0], round(self.y)-new_h//2+offset[1]))

    def get_width(self):
        return self.surface.get_width()*self.w_ratio

    def set_width(self, width):
        self.w_ratio = width/self.surface.get_width()

    def get_height(self):
        return self.surface.get_height()*self.h_ratio

    def set_height(self, height):
        self.h_ratio = height/self.surface.get_height()

    def get_pos(self):
        return self.x, self.y

    def set_pos(self, pos):
        self.x = pos[0]
        self.y = pos[1]

    width = property(get_width, set_width)
    height = property(get_height, set_height)
    pos = property(get_pos, set_pos)