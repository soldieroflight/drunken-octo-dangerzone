import pygame
import math, os, sys
from physics.mathutils import *
from physics.collisionutils import *
from physics.globals import *
from levels import *
from baselevel import *
from input import *
from camera import *


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
    
    def sync_transform(self):
        self.transform.set_translation(self.rigidbody.position)
        

class Projectile(PhysicalObject):
    def __init__(self, pos=Vector2(0,0), dir=Vector2(0,0)):
        super().__init__(pos)
        self.radius = 3
        self.rigidbody = AABB(pos, self.radius, self.radius)
        self.initialSpeed = 500
        self.rigidbody.velocity = Vector2(dir.x * self.initialSpeed, dir.y)
        self.rigidbody.callback = self.on_collision
        self.rigidbody.owner = self
        # Checked externally for cleanup.
        self.expired = False
        
    def update(self, deltaTime):
        super().update(deltaTime)
        self.rigidbody.add_force(GRAVITY)
        self.rigidbody.update(deltaTime)
        self.rigidbody.clear_forces()
        
    def debug_draw(self, camera):
        camera.circle((255,255,255), self.rigidbody.position.safe_pos(), self.radius)
        
    def on_collision(self, other):
        self.expired = True
    
        
class Player(PhysicalObject):
    def __init__(self, pos=Vector2(0,0)):
        super().__init__(pos)
        self.keyListener = keyboard.Keyboard()
        self.rigidbody = AABB(pos, 30, 60)
        self.rigidbody.owner = self
        self.speed = 120.0 # units/second
        self.jumpForce = Vector2(0.0, -35000.0)
        self.facing = 1.0
        
    def update(self, deltaTime):
        super().update(deltaTime)
        movementVector = Vector2(0.0, 0.0)
        
        if (self.keyListener.get_key_pressed('space')) and self.rigidbody.grounded:
            self.rigidbody.add_force(self.jumpForce)
            self.rigidbody.grounded = False
        
        if not self.rigidbody.grounded:
            self.rigidbody.add_force(PLAYER_GRAVITY)
        
        # Decouple rigidbody motion from player controlled motion.
        bodyPosition = self.rigidbody.position.copy()
        # Step the player's physics.
        self.rigidbody.update(deltaTime)
        # Get the difference in rigidbody movement.
        movementVector += self.rigidbody.position - bodyPosition
        
        # Handle basic movement.
        if (self.keyListener.get_key_pressed('a') or self.keyListener.get_key_pressed('left')):
            movementVector.x -= self.speed * deltaTime
            self.facing = -1.0
        if (self.keyListener.get_key_pressed('d') or self.keyListener.get_key_pressed('right')):
            movementVector.x += self.speed * deltaTime
            self.facing = 1.0
            
        self.transform.translate(movementVector)
        
        # Synchronize the rigidbody.
        self.rigidbody.position = self.transform.get_translation()
        self.rigidbody.clear_forces()
        
        # Handle firing of projectiles.
        if (self.keyListener.get_key_pressed('f')):
            proj = Projectile(self.transform.get_translation().copy(), Vector2(self.facing, 0.0))
            globalProjectiles.append(proj)
         
    def debug_draw(self, camera):
        self.rigidbody.draw(camera)
        
        
class Platform(PhysicalObject):
    def __init__(self, pos=Vector2(0,0), width=0, height=0):
        super().__init__(pos)
        self.rigidbody = AABB(pos, width, height)
        self.rigidbody.owner = self
        self.rigidbody.useDynamics = False
        
    def debug_draw(self, camera):
        self.rigidbody.draw(camera)
        
from game import *

if __name__ == "__main__":
    pygame.init()
    keyboard.initialize()
    
    screen = pygame.display.set_mode((640,480))
    clock = pygame.time.Clock()

    level = TestLevel()
    game = Game(screen)
    game.load_level(level)

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