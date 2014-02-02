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
    
class PlatformTest(Level):
    def __init__(self):
        super().__init__()
        self.worldSize = Vector2(1200, 600)
        self.ground = 500
        self.playerStart = Vector2(100, 400)
        
    def load(self):
        super().load()
        
        self.platforms.append(Platform(Vector2(0, 0), 100, 1000))
        self.platforms.append(Platform(Vector2(350, 475), 50, 50))
        self.platforms.append(Platform(Vector2(500, 450), 100, 100))
        self.platforms.append(Platform(Vector2(700, 450), 100, 100))
        self.platforms.append(Platform(Vector2(950, 450), 100, 100))
        self.platforms.append(Platform(Vector2(100, 425), 100, 150))
        
    
class Level1(Level):
    def __init__(self):
        super().__init__()
        self.worldSize = Vector2(1200, 800)
        self.ground = 900
        self.playerStart = Vector2(300, 500)
        
    def load( self):
        super().load()
        
        self.platforms.append(Platform(Vector2(0, 500), 50, 1000))
        self.platforms.append(Platform(Vector2(50, 50), 500, 50))
        self.platforms.append(Platform(Vector2(550, 100), 200, 100))
        self.platforms.append(Platform(Vector2(750, 150), 50, 150))
        self.platforms.append(Platform(Vector2(800, 200), 50, 200))
        self.platforms.append(Platform(Vector2(850, 250), 250, 250))