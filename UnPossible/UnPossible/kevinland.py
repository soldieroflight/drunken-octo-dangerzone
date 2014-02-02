import pygame
import math, os, sys
from physics.mathutils import *
from physics.collisionutils import *
from physics.globals import *
from input import *
from camera import *

globalProjectiles = []

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
        
    def update(self, deltaTime):
        super().update(deltaTime)
        self.rigidbody.add_force(GRAVITY)
        self.rigidbody.update(deltaTime)
        self.rigidbody.clear_forces()
        
    def debug_draw(self, camera):
        camera.circle((255,255,255), self.rigidbody.position.safe_pos(), self.radius)
    
        
class Player(PhysicalObject):
    def __init__(self, pos=Vector2(0,0)):
        super().__init__(pos)
        self.keyListener = keyboard.Keyboard()
        self.rigidbody = AABB(pos, 30, 60)
        self.speed = 120.0 # units/second
        self.jumpForce = Vector2(0.0, -20000.0)
        self.gravity = Vector2(0.0, 980.0)
        self.facing = 1.0
        
    def update(self, deltaTime):
        super().update(deltaTime)
        movementVector = Vector2(0.0, 0.0)
        
        if (self.keyListener.get_key_pressed('space')) and self.rigidbody.grounded:
            self.rigidbody.add_force(self.jumpForce)
            self.rigidbody.grounded = False
        
        if not self.rigidbody.grounded:
            self.rigidbody.add_force(self.gravity)
        
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
        self.rigidbody.useDynamics = False
        
    def debug_draw(self, camera):
        self.rigidbody.draw(camera)
    

if __name__ == "__main__":
    pygame.init()
    keyboard.initialize()
    
    player = Player(Vector2(100, 400))
    
    platform1 = Platform(Vector2(200, 330), 100, 10)
    platform2 = Platform(Vector2(300, 280), 100, 10)
    platforms = [platform1, platform2]

    # set up pygame stuff
    screen = pygame.display.set_mode((640,480))
    clock = pygame.time.Clock()
    camera = Camera(Vector2(640, 480), Vector2(800, 600), screen)
    
    ground = Plane(Vector2(240, 450), Vector2(0.0, -1.0))
    
    # Reasonable initial dt.
    ticks = 16

    while True:
        t = pygame.time.get_ticks()
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
                
        if ticks < 1:
            ticks = 16
        ticks = 1.0/ticks
        deltaTime = clock.get_time()/1000.0
                
        player.update(deltaTime)
        for proj in globalProjectiles:
            proj.update(deltaTime)
        camera.update(player.rigidbody.position)
        
        aabb_vs_plane(player.rigidbody, ground)
        for platform in platforms:
            aabb_vs_aabb(player.rigidbody, platform.rigidbody)
        
        player.sync_transform()

        player.debug_draw(camera)
        for platform in platforms:
            platform.debug_draw(camera)
        ground.draw(camera)
        
        for proj in globalProjectiles:
            proj.debug_draw(camera)
        
        pygame.display.update()
        ticks = pygame.time.get_ticks() - t