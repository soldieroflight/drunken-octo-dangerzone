from baseobjects import *
from player import *

class FloorSwitch(PhysicalObject):
    def __init__(self, position, width, height, targets):
        super().__init__(position)
        self.targets = targets
        self.rigidbody = AABB(position, width, height)
        self.rigidbody.solid = False
        self.rigidbody.owner = self
        self.rigidbody.callback = self.trigger
        self.rigidbody.solid = False
        
    def update(self, deltaTime):
        super().update(deltaTime)

    def trigger(self, other):
        for target in self.targets:
            target.trigger()
        return False

    def debug_draw(self, camera):
        self.rigidbody.draw(camera)