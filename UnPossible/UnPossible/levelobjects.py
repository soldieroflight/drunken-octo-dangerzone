from baseobjects import *

class Platform(PhysicalObject):
    def __init__(self, pos=Vector2(0,0), width=0, height=0):
        super().__init__(pos)
        self.rigidbody = AABB(pos, width, height)
        self.rigidbody.owner = self
        self.rigidbody.useDynamics = False
        
    def debug_draw(self, camera):
        self.rigidbody.draw(camera)

class TimeBubble(object):
    def __init__(self, timeScale, pos, size):
        self.timeScale = timeScale
        self.pos = pos
        self.size = size

    def contains(self, pos):
        return dist(self.pos, pos) < self.size

    def draw(self, camera):
        camera.circle((255, 255, 255), (self.pos.x, self.pos.y), self.size, 1)