import pygame
import anime
import random

pygame.init()

screen = pygame.display.set_mode((800, 600))
squares = []
entrance = {
    'x' : -50,
    'y' : 300
}
exit = {
    'x' : 1000,
    'y' : 300
}
episode = anime.Episode(entrance, exit)
playing = True

while playing:
    mx, my = pygame.mouse.get_pos()
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            playing = False
        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_EQUALS:
                tmp_surf = pygame.Surface((100, 100))
                tmp_surf.fill((random.randint(0, 255),
                               random.randint(0, 255),
                               random.randint(0, 255)))
                tmp_anime = anime.Anime(tmp_surf, random.randint(200, 600),
                                        random.randint(50, 550))
                tmp_anime.set_filter('x', anime.filter.Spring(0.1, 0.5))
                tmp_anime.set_filter('y', anime.filter.Spring(0.1, 0.5))
                squares.append(tmp_anime)
            elif e.key == pygame.K_MINUS:
                if squares:
                    squares.pop(0)

    screen.fill((255, 255, 255))
    episode.update(squares)
    episode.render(squares, screen)
    pygame.display.flip()
    pygame.time.wait(10)

pygame.quit()