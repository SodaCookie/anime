import pygame
import pygame.gfxdraw
import anime
from anime.math.parametric import Parametric2D
from anime.math.polar import Polar
import random
from collections import deque
import math

pygame.init()


MAX = 5000
x = lambda t: math.sin(t)*(math.e**math.cos(t)-2*math.cos(4*t)-math.sin(t/12)**5)
y = lambda t: math.cos(t)*(math.e**math.cos(t)-2*math.cos(4*t)-math.sin(t/12)**5)
s = lambda phi: phi*0.5

screen = pygame.display.set_mode((800, 600))
surf = pygame.image.load("anime/demo/images/image1.png").convert_alpha()
path = Parametric2D(x, y)
spiral = Polar(s)
pixels = deque(maxlen=MAX)

a = anime.Anime(surf, 0, 0)
a.set_renderer('w_ratio', anime.renderer.wratio_smooth_renderer)
a.set_renderer('h_ratio', anime.renderer.hratio_smooth_renderer)
a.w_ratio = 0.2
a.h_ratio = 0.2

playing = True
counter = 0

def draw_pixel(pixel):
    pygame.gfxdraw.pixel(screen, round(pixel[0]), round(pixel[1]), (255, 255, 255))

while playing:
    mx, my = pygame.mouse.get_pos()
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            playing = False

    screen.fill((0,0,0))
    list(map(draw_pixel, pixels))

    path.t += 0.02
    spiral.phi += 0.01
    x, y = path.get_pos()
    x, y = x*70+400, y*70+300

    if len(pixels) == MAX:
        pixels.popleft()
    pixels.append((x, y))

    a.x, a.y = x, y
    spiral.update()
    path.update()
    a.update()
    a.render(screen)
    pygame.display.flip()
    pygame.time.wait(5)

pygame.quit()