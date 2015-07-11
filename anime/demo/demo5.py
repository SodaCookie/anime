import pygame
import anime
import random
import math
pygame.init()

screen = pygame.display.set_mode((800, 600))
surf = pygame.image.load("anime/demo/images/image1.png").convert_alpha()
a = anime.Anime(surf, 400, 300)
a.set_renderer('w_ratio', anime.renderer.wratio_smooth_renderer)
a.set_renderer('h_ratio', anime.renderer.hratio_smooth_renderer)

holding = False
mouse_down = False
resetting = False
playing = True
offsetx = 0
offsety = 0

while playing:
    mx, my = pygame.mouse.get_pos()
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            playing = False
        elif e.type == pygame.MOUSEBUTTONDOWN:
            mouse_down = True
            offsetx, offsety = mx, my
            if a.collide_point_alpha(mx, my, 0):
                holding = True

        elif e.type == pygame.MOUSEBUTTONUP:
            mouse_down = False
            holding = False

        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_r:
                resetting = True
                a.set_filter("w_ratio", anime.filter.spring, done=anime.filter.done_almost_equal)
                a.set_filter("h_ratio", anime.filter.spring, done=anime.filter.done_almost_equal)
                a.set_filter("angle", anime.filter.spring, done=anime.filter.done_almost_equal)
                a.w_ratio = 1
                a.h_ratio = 1
                a.angle = 0

    screen.fill((255,255,255))
    if holding and not resetting:
        ratio = math.sqrt((400-mx)**2+(400-my)**2)/math.sqrt((400-offsetx)**2+(300-offsety)**2)
        a.w_ratio = ratio
        a.h_ratio = ratio
    if not holding and mouse_down and not resetting:
        angle = math.atan2(offsety-400, offsetx-300)-math.atan2(my-400, mx-300)
        a.angle = math.degrees(angle)
    if resetting:
        if not a.is_dirty():
            resetting = False
            a.remove_filter("w_ratio")
            a.remove_filter("h_ratio")
            a.remove_filter("angle")

    a.update()
    a.render(screen)
    pygame.display.flip()
    pygame.time.wait(10)

pygame.quit()