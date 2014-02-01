import pygame
import math, os, sys

from physics.mathutils import *
from events.link import Link
from input import *

vec = Vector2(0, 0)

pygame.init()
keyboard.initialize()

screen = pygame.display.set_mode((1024,768))
clock = pygame.time.Clock()

_link2 = Link([], (Vector2(200.0, 100.0), Vector2(200.0, 5.0)), 60.0)
_link3 = Link([], (Vector2(200.0, 100.0), Vector2(200.0, 500.0)), 10.0)

_link = Link([_link2, _link3], (Vector2(5.0, 5.0), Vector2(100.0, 5.0), Vector2(100.0, 100.0), Vector2(200.0, 100.0)), 10.0)
_link.trigger()

while True:
    clock.tick(30)
    screen.fill((0,0,0))
    
    for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
    deltaTime = clock.get_time()/1000.0
    if deltaTime > 0.5:
        deltaTime = 0.5

    _link.update(deltaTime)
    _link2.update(deltaTime)
    _link3.update(deltaTime)
    _link.draw(screen)
    _link2.draw(screen)
    _link3.draw(screen)

    pygame.display.update()
