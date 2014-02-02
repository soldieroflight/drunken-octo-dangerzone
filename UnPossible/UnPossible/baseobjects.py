import pygame
import math, os, sys
from physics.mathutils import *
from physics.collisionutils import *
from physics.globals import *
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
        
    def sync_transform(self):
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