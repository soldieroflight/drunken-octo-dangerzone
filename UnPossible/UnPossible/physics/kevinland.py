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
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mousex, mousey = pygame.mouse.get_pos()
                    point = Vector2(mousex,mousey)
                    if box1.contains(point): grabbed_box = box1
                    elif box2.contains(point): grabbed_box = box2
                    if not grabbed_box is None: mousex,mousey = pygame.mouse.get_rel()
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    grabbed_box = None
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        pygame.display.update()