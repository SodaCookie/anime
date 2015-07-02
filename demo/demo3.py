import pygame
import anime
import random
pygame.init()

screen = pygame.display.set_mode((800, 600))
test_surface = pygame.Surface((300, 300), pygame.SRCALPHA)
test_surface2 = pygame.Surface((100, 100), pygame.SRCALPHA)
test_surface.fill((0, 0, 0, 255))
test_surface2.fill((255, 0, 0, 255))

a = anime.Anime(test_surface, 400, 300)
b = anime.Anime(test_surface2, 150, 150)
a.set_filter('w_ratio', anime.filter.spring)
a.set_filter('h_ratio', anime.filter.spring)
a.set_filter('opacity', anime.filter.linear, 5)
b.set_owner(a)
counter = 2
other = 0
playing = True

while playing:
    mx, my = pygame.mouse.get_pos()
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            playing = False
        if e.type == pygame.MOUSEBUTTONDOWN:
            if b.collide_point(mx, my):
                counter = 4 if counter%4 else 2
                if counter == 2:
                    a.width = 200
                    a.height = 200
                else:
                    a.width = 500
                    a.height = 500
            else:
                if other%2:
                    a.opacity = 0
                else:
                    a.opacity = 255
                other += 1

    screen.fill((255,255,255))
    a.update()
    b.update()
    a.render(screen)
    pygame.display.flip()
    pygame.time.wait(10)

pygame.quit()