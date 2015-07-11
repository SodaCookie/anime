import pygame
import pygame.gfxdraw
import anime
from anime.math.bezier import CubicBezier, QuadraticBezier
import random
import math
pygame.init()

screen = pygame.display.set_mode((800, 600))
surf = pygame.image.load("anime/demo/images/image1.png").convert_alpha()
path1 = CubicBezier([(0, 0), (56, 500), (300, 20), (800, 600)])
path1.set_filter('t', anime.filter.linear, 0.02)
path2 = QuadraticBezier([(0, 0), (0, 600), (800, 600)])
path2.set_filter('t', anime.filter.linear, 0.02)
path = path1
a = anime.Anime(surf, 0, 0)
a.set_filter('x', anime.filter.spring)
a.set_filter('y', anime.filter.spring)
a.set_renderer('w_ratio', anime.renderer.wratio_smooth_renderer)
a.set_renderer('h_ratio', anime.renderer.hratio_smooth_renderer)
a.w_ratio = 0.5
a.h_ratio = 0.5

playing = True
counter = 0

while playing:
    mx, my = pygame.mouse.get_pos()
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            playing = False
        elif e.type == pygame.MOUSEBUTTONDOWN:
            if counter % 2:
                path.t = 0
            else:
                path.t = 1
            counter += 1
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_r:
                if path == path1:
                    path = path2
                else:
                    path = path1

    screen.fill((255,255,255))
    pygame.gfxdraw.bezier(screen, path.path, len(path.path), (255, 0 , 0))
    a.x, a.y = path.get_pos()
    path.update()
    a.update()
    a.render(screen)
    pygame.display.flip()
    pygame.time.wait(10)

pygame.quit()