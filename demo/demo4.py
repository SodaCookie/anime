import pygame
import anime
import random
pygame.init()

screen = pygame.display.set_mode((800, 600))
surfs = [pygame.Surface((100, 100), pygame.SRCALPHA) for i in range(9)]
for s in surfs:
    s.fill((random.randint(0, 255), random.randint(0, 255),
        random.randint(0, 255)))

animes = [anime.Anime(s, 0, 0) for s in surfs]
for a in animes:
    a.set_filter('x', anime.filter.Spring(0.2, 0.6))
    a.set_filter('y', anime.filter.Spring(0.2, 0.6))

playing = True
offsetx = 0
offsety = 0
on_hand = None

while playing:
    mx, my = pygame.mouse.get_pos()
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            playing = False
        if e.type == pygame.MOUSEBUTTONDOWN:
            for a in animes:
                if a.collide_point(mx, my):
                    animes.remove(a)
                    on_hand = a
                    rect = a.get_bounding_rect()
                    offsetx = mx - rect.center[0]
                    offsety = my - rect.center[1]

        elif e.type == pygame.MOUSEBUTTONUP:
            if on_hand:
                animes.append(on_hand)
                on_hand = None

    screen.fill((255,255,255))
    for i, a in enumerate(animes):
        a.x = 180 + 120 * (i % 3)
        a.y = 180 + 120 * (i // 3)
        a.update()
        a.render(screen)
    if on_hand:
        on_hand.x = mx + offsetx
        on_hand.y = my + offsety
        on_hand.update()
        on_hand.render(screen)
    pygame.display.flip()
    pygame.time.wait(10)

pygame.quit()