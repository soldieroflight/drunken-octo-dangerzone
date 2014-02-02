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
        
        self.platforms.append(Platform(None, 100, 10, Vector2(200, 390)))
        self.platforms.append(Platform(None, 100, 10, Vector2(300, 320)))
        self.platforms.append(Platform(None, 100, 10, Vector2(400, 270)))
        self.platforms.append(Platform(None, 100, 10, Vector2(500, 220)))
        self.platforms.append(Platform(None, 100, 10, Vector2(600, 170)))
        self.platforms.append(Platform(None, 100, 10, Vector2(700, 120)))
        self.platforms.append(Platform(None, 100, 10, Vector2(800, 70)))

        self.links.append(Link([], (Vector2(400, 500), Vector2(400, 300)), 20.0))
        self.switches.append(FloorSwitch(Vector2(400, 500), 100, 10, self.links))
    
class PlatformTest(Level):
    def __init__(self):
        super().__init__()
        self.worldSize = Vector2(1200, 600)
        self.ground = 500
        self.playerStart = Vector2(300, 400)
        
    def load(self):
        super().load()
        
        self.platforms.append(Platform(None, 100, 1000, Vector2(0, 0)))
        self.platforms.append(Platform(None, 50, 50, Vector2(350, 475)))
        self.platforms.append(Platform(None, 100, 100, Vector2(500, 450)))
        self.platforms.append(Platform(None, 100, 100, Vector2(700, 450)))
        self.platforms.append(Platform(None, 100, 100, Vector2(950, 450)))
        self.platforms.append(Platform(None, 100, 150, Vector2(100, 425)))
        
    
class Level1(Level):
    def __init__(self):
        super().__init__()
        self.worldSize = Vector2(9000, 800)
        self.ground = 900
        self.playerStart = Vector2(200, 700)
        
    def load( self):
        super().load()
        
        self.platforms.append(Platform(Vector2(0, 0), 50, 1000))
        self.platforms.append(Platform(Vector2(50, 100), 500, 50))
        self.platforms.append(Platform(Vector2(550, 100), 300, 100))
        self.platforms.append(Platform(Vector2(850, 100), 50, 150))
        self.platforms.append(Platform(Vector2(900, 100), 50, 200))
        self.platforms.append(Platform(Vector2(950, 100), 250, 250))