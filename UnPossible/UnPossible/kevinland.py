import pygame
import math, os, sys
from physics.mathutils import *
from physics.collisionutils import *
from physics.globals import *
from performance import framerate
from baselevel import *
from input import *
from camera import *
from game import *
from levels import *

WINDOW_SIZE = (640, 480)
TARGET_FRAMERATE = 60

if __name__ == "__main__":
    pygame.init()
    
    screen = pygame.display.set_mode(WINDOW_SIZE)
    clock = pygame.time.Clock()
    
    framerateMonitor = framerate.FramerateMonitor(TARGET_FRAMERATE)
    framerateFont = pygame.font.Font(None,20)

    keyboard.initialize()

    level = Level1()
    game = Game(screen)
    game.load_level(level)

    game.camera.debug_set_background([(640, 480), (900, 550), (1200, 600)])

    game.timeBubbles.append(TimeBubble(0.5, Vector2(400, 500), 50))

    # set up pygame stuff

    while True:
        clock.tick(TARGET_FRAMERATE)
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
                
        # get and cap deltaTime
        deltaTime = min( clock.get_time()/1000.0, 0.1 )
                
        game.update(deltaTime)
        game.draw()
        
        framerateMonitor.update(deltaTime)
        fps = framerateFont.render("%.3f" % framerateMonitor.average,1,(255,255,255))
        fpsRect = fps.get_rect()
        fpsRect.center = (600,465)
        screen.blit(fps,fpsRect)
        
        pygame.display.update()