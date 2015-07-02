import pygame

def angle_renderer(surface, angle):
    return pygame.transform.rotate(surface, angle)

def wratio_renderer(surface, wratio):
    w, h = surface.get_size()
    return pygame.transform.scale(surface, (round(w*wratio), h))

def hratio_renderer(surface, hratio):
    w, h = surface.get_size()
    return pygame.transform.scale(surface, (w, round(h*hratio)))

def opacity_renderer(surface, opacity):
    if opacity == 255:
        return surface
    if surface.get_flags() & pygame.SRCALPHA:
        surface.fill((0, 0, 0, abs(opacity-255)), special_flags=pygame.BLEND_RGBA_SUB)
    else:
        surface.set_alpha(opacity)
    return surface