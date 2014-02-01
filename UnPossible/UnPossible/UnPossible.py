import pygame
import math, os, sys

from physics import *
#import physics.mathutils
#from physics.mathutils import *
#from collisionutils import *

vec = mathutils.Vector2(0, 0)

pygame.init()

# set up pygame stuff
screen = pygame.display.set_mode((1024,768))
clock = pygame.time.Clock()

while True:
    # pygame stuff
    clock.tick(30)
    screen.fill((0,0,0))
