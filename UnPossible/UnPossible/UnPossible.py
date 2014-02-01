import pygame
import math, os, sys

from physics.mathutils import *
from input import *

vec = Vector2(0, 0)

pygame.init()
keyboard.initialize()

screen = pygame.display.set_mode((1024,768))
clock = pygame.time.Clock()

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
                
    pygame.display.update()
