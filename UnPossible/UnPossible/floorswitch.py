from baseobjects import *
from player import *

class FloorSwitch(PhysicalObject):
    def __init__(self, position, width, height, targets):
        self.targets = targets
        self.rigidbody = AABB(position, width, height)
        self.rigidbody.owner = self
        self.rigidbody.callback = lambda collider: self.trigger()
        
    def update(self, deltaTime, timeBubbles):
        super().update(deltaTime, timeBubbles)

    def trigger(self):
        for target in self.targets:
            target.trigger()
        return True

    def debug_draw(self, camera):
        self.rigidbody.draw(camera)