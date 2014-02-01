import pygame
import math, os, sys
from physics.mathutils import *
from physics.collisionutils import *
from input import *

class GameObject(object):
    def __init__(self, pos=Vector2(0,0)):
        assert (isinstance(pos, Vector2))
        self.transform = Matrix2D()
        self.parent = None
        self.setup(pos)
        
    def setup(self, pos):
        self.transform.translate_x(pos.x)
        self.transform.translate_y(pos.y)
        
    def update(self, deltaTime):
        pass
        
        
class PhysicalObject(GameObject):
    def __init__(self, pos=Vector2(0,0)):
        super().__init__(pos)
        self.rigidbody = None
    
        
class Player(PhysicalObject):
    def __init__(self, pos=Vector2(0,0)):
        super().__init__(pos)
        self.keyListener = keyboard.Keyboard()
        self.rigidbody = AABB(pos, 30, 60)
        self.speed = 100.0 # units/second
        self.gravity = Vector2(0.0, 980.0)
        
    def update(self, deltaTime):
        super().update(deltaTime)
        # Always add gravity.
        self.rigidbody.add_force(self.gravity)
        
        # Decouple rigidbody motion from player controlled motion.
        bodyPosition = self.rigidbody.position.copy()
        # Step the player's physics.
        self.rigidbody.update(deltaTime)
        # Get the difference in rigidbody movement.
        movementVector = self.rigidbody.position - bodyPosition
        
        # Handle basic movement.
        if (self.keyListener.get_key_pressed('a')):
            movementVector.x -= self.speed * deltaTime
        if (self.keyListener.get_key_pressed('d')):
            movementVector.x += self.speed * deltaTime
            
        self.transform.translate(movementVector)
        
        # Synchronize the rigidbody.
        self.rigidbody.position = self.transform.get_translation()
        self.rigidbody.clear_forces()
         
    def debug_draw(self, screen):
        self.rigidbody.draw(screen)
    

if __name__ == "__main__":
    pygame.init()
    keyboard.initialize()
    
    player = Player(Vector2(100, 400))

    # set up pygame stuff
    screen = pygame.display.set_mode((640,480))
    clock = pygame.time.Clock()
    
    ground = Plane(Vector2(240, 450), Vector2(0.0, -1.0))
    
    # Reasonable initial dt.
    ticks = 16

    while True:
        t = pygame.time.get_ticks()
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
                
        if ticks < 1:
            ticks = 16
        ticks = 1.0/ticks
        deltaTime = clock.get_time()/1000.0
                
        player.update(deltaTime)
        
        aabb_vs_plane(player.rigidbody, ground)
        
        player.debug_draw(screen)
        ground.draw(screen)
        
        pygame.display.update()
        ticks = pygame.time.get_ticks() - t