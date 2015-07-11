"""
This module defines the Anime class.
"""

from collections import OrderedDict

from pygame import Surface

from anime.core.rubberband import RubberBand
import anime.core.renderer as renderer
import anime.core.reducer as reducer

class Anime(RubberBand):
    """Anime is a wrapper around RubberBand to help define common
    attributes used in animation. It also handles the rendering
    of a pygame Surface onto another surface."""

    def __init__(self, surface, x, y):
        """Takes a surface, x and y. The surface is used for rendering.
        X and Y are used to define the position where the surface will
        be drawn. All Anime surfaces will be drawn anchored to center
        to allow smooth rotation."""
        super().__init__()
        object.__setattr__(self, "_renderers", OrderedDict())
        object.__setattr__(self, "_blit_rect", None)
        object.__setattr__(self, "_blit_surf", None)

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
        self.set_renderer('opacity', renderer.opacity_renderer)
        self.set_reducer('opacity', reducer.bot_level_reducer)

    def set_renderer(self, name, renderer):
        """Sets a renderer to the given attribute name."""
        self._renderers[name] = renderer

    def get_renderer(self, name):
        """Returns the renderer of the attribute name."""
        return self._renderers.get(name)

    def render(self, surface, offset=(0, 0)):
        """Given a surface. Anime will draw its wrapped surface onto the
        given surface at its current x and y coordinates. All renderers
        will be called to generate the proper image."""
        tmp_surf = self.surface.copy()
        prev_w, prev_h = tmp_surf.get_size()

        for name, renderer in self._renderers.items():
            tmp_surf = renderer(tmp_surf, self.get_absolute_value(name))

        new_w, new_h = tmp_surf.get_size()
        offsetx, offsety = (new_w - prev_w) // 2, (new_h - prev_h) // 2

        for child in self.get_children():
            child.render(tmp_surf, (offsetx, offsety))

        object.__setattr__(self, "_rendered", tmp_surf)

        rect = surface.blit(tmp_surf,
            (round(self.x)-new_w//2+offset[0], round(self.y)-new_h//2+offset[1]))

        object.__setattr__(self, "_blit_rect", rect)
        object.__setattr__(self, "_blit_surf", tmp_surf) #TODO can be used for optimization

    def get_bounding_rect(self):
        """Returns a pygame Rect describing the bounding rectangle where
        surface is drawn. If this object has not yet been drawn than None
        is returned."""
        if self._blit_rect is None:
            return None
        if self.get_owner():
            rect = self.get_owner().get_bounding_rect()
            if rect is None:
                return None
            rect.size = (self.width, self.height)
            rect.topleft = (rect.topleft[0] + self._blit_rect.topleft[0], rect.topleft[1] + self._blit_rect.topleft[1])
            return rect
        else:
            return self._blit_rect

    def collide_point(self, x, y):
        """Check to see if given point x and y is inside bounding rectangle
        of the drawn object"""
        if self._blit_rect:
            return self.get_bounding_rect().collidepoint(x, y)
        return False

    def collide_point_alpha(self, x, y, threshold=15):
        """Check to see if given point x and y is inside bounding rectangle
        of the drawn object as well as the given point's alpha is above the
        given threshold."""
        if self._blit_rect:
            rect = self.get_bounding_rect()
            if rect.collidepoint(x, y):
                offsetx, offsety = x - rect.topleft[0], y - rect.topleft[1]
                return self._blit_surf.get_at((offsetx, offsety))[3] \
                    > threshold
        return False

    def get_width(self):
        """Returns the current width of the object."""
        return self.surface.get_width()*self.get_absolute_value('w_ratio')

    def set_width(self, width):
        """Sets the current width of the object"""
        self.w_ratio = width/self.surface.get_width()

    def get_height(self):
        """Returns the current height of the object."""
        return self.surface.get_height()*self.get_absolute_value('h_ratio')

    def set_height(self, height):
        """Sets the current height of the object"""
        self.h_ratio = height/self.surface.get_height()

    def get_pos(self):
        """Returns the current position of the object."""
        return self.x, self.y

    def set_pos(self, pos):
        """Sets the current position of the object"""
        self.x = pos[0]
        self.y = pos[1]


    # Defines properties of the object
    width = property(get_width, set_width)
    height = property(get_height, set_height)
    pos = property(get_pos, set_pos)