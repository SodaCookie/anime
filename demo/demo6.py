import pygame
import anime
import math
from random import randint

pygame.init()

screen = pygame.display.set_mode((800, 600))
test_surface = pygame.Surface((50, 50), pygame.SRCALPHA)
test_surface.fill((0, 0, 0, 255))

a = anime.Anime(test_surface, 400, 300)
a.set_filter('x', anime.filter.exponential)
a.set_filter('y', anime.filter.exponential)

animes = [anime.Anime(test_surface, randint(0, 800), randint(0, 600)) for i in range (200)]

playing = True
holding = False

while playing:
    mx, my = pygame.mouse.get_pos()

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            playing = False
        elif e.type == pygame.MOUSEBUTTONDOWN:
            holding = True
        elif e.type == pygame.MOUSEBUTTONUP:
            holding = False

    screen.fill((255,255,255))
    a.angle = math.degrees(math.atan2(a.y-my, mx-a.x))
    for anime_thing in animes:
        anime_thing.angle = math.degrees(math.atan2(anime_thing.y-my, mx-anime_thing.x))
    if holding:
        a.pos = (mx, my)
    else:
        a.pos = a.pos
    a.update()
    for anime_thing in animes:
        anime_thing.update()
        anime_thing.render(screen)
    a.render(screen)
    pygame.display.flip()
    # pygame.time.wait(10)

pygame.quit()