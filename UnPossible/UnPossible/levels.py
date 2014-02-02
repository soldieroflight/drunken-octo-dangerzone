from levelobjects import *
from baselevel import *
from floorswitch import *
from link import *

# This is a sample level.
class TestLevel(Level):
    def __init__(self):
        super().__init__()
        self.worldSize = Vector2(1200, 600)
        self.ground = 500
        self.playerStart = Vector2(100, 400)
        
    def load(self):
        super().load()
        
        self.platforms.append(Platform(Vector2(200, 370), 100, 10))
        self.platforms.append(Platform(Vector2(300, 320), 100, 10))
        self.platforms.append(Platform(Vector2(400, 270), 100, 10))
        self.platforms.append(Platform(Vector2(500, 220), 100, 10))
        self.platforms.append(Platform(Vector2(600, 170), 100, 10))
        self.platforms.append(Platform(Vector2(700, 120), 100, 10))
        self.platforms.append(Platform(Vector2(800, 70), 100, 10))

        self.links.append(Link([], (Vector2(400, 500), Vector2(400, 300)), 20.0))
        self.switches.append(FloorSwitch(Vector2(400, 500), 100, 10, self.links))