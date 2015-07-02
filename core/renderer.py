import pygame

def angle_renderer(surface, angle):
    return pygame.transform.rotate(surface, angle)

def wratio_renderer(surface, wratio):
    w, h = surface.get_size()
    return pygame.transform.scale(surface, (round(w*wratio), h))

def hratio_renderer(surface, hratio):
    w, h = surface.get_size()
    return pygame.transform.scale(surface, (w, round(h*hratio)))