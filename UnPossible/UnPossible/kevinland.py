import pygame
import math, os, sys
from physics.mathutils import *
from physics.collisionutils import *
from physics.globals import *
from baselevel import *
from input import *
from camera import *
from game import *
from levels import *

if __name__ == "__main__":
    pygame.init()
    
    screen = pygame.display.set_mode((640,480))
    clock = pygame.time.Clock()

    keyboard.initialize()

    level = Level1()
    game = Game(screen)
    game.load_level(level)

    game.camera.debug_set_background((700, 500))

    game.timeBubbles.append(TimeBubble(0.5, Vector2(400, 500), 50))

    # set up pygame stuff

    while True:
        clock.tick(60)
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
                
        deltaTime = clock.get_time()/1000.0
                
        game.update(deltaTime)
        game.draw()
        
        pygame.display.update()