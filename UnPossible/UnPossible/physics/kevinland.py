import pygame
import math, os, sys
from mathutils import *
from collisionutils import *

class GameObject(object):
    def __init__(self, pos=Vector2(0,0)):
        self.transform = Matrix2D()
        self.setup(pos)
        
    def setup(self, pos):
        self.transform.translate_x(pos.x)
        self.transform.translate_y(pos.y)
        
class Player(GameObject):
    def __init__(self, pos=Vector2(0,0)):
        super().__init__(pos)
        
    

if __name__ == "__main__":
    pygame.init()

    # set up pygame stuff
    screen = pygame.display.set_mode((640,480))
    clock = pygame.time.Clock()

    while True:
        clock.tick(30)
        screen.fill((0,0,0))
        
        # event handling
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        pygame.display.update()