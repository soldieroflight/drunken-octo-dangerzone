from levelobjects import *
from baselevel import *
from enemies import *
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
        self.platforms.append(Platform(Vector2(950, 100), 350, 250))
        self.platforms.append(Platform(Vector2(1300, 100), 50, 200))
        self.platforms.append(Platform(Vector2(1350, 100), 300, 250))
        self.platforms.append(Platform(Vector2(1650, 100), 100, 200))
        self.platforms.append(Platform(Vector2(1750, 100), 400, 250))
        self.platforms.append(Platform(Vector2(2150, 100), 50, 175))
        self.platforms.append(Platform(Vector2(2200, 100), 50, 100))
        self.platforms.append(Platform(Vector2(2250, 100), 300, 250))
        self.platforms.append(Platform(Vector2(2550, 100), 50, 175))
        self.platforms.append(Platform(Vector2(2600, 100), 50, 100))
        self.platforms.append(Platform(Vector2(2675, 325), 100, 25)) #Platform 1
        self.platforms.append(Platform(Vector2(2875, 325), 100, 25)) #Platform 2
        self.platforms.append(Platform(Vector2(2650, 100), 425, 25))
        self.platforms.append(Platform(Vector2(3075, 100), 325, 250))
        self.platforms.append(Platform(Vector2(3500, 100), 100, 250))
        self.platforms.append(Platform(Vector2(3700, 100), 100, 250))
        self.platforms.append(Platform(Vector2(3900, 100), 200, 250))
        self.platforms.append(Platform(Vector2(4100, 100), 500, 125))
        self.platforms.append(Platform(Vector2(4150, 375), 400, 25)) #Moving Platform 1
        self.platforms.append(Platform(Vector2(4600, 100), 200, 300))
        self.platforms.append(Platform(Vector2(4900, 375), 300, 25)) #Moving Platform 2
        self.platforms.append(Platform(Vector2(5200, 375), 300, 25)) #Moving Platform 3
        self.platforms.append(Platform(Vector2(5600, 100), 400, 300))
        self.platforms.append(Platform(Vector2(5850, 425), 100, 175)) #Moving Platform 4
        self.platforms.append(Platform(Vector2(6000, 100), 150, 500)) #Moving Platform 4
        
        basicEnemy = BaseEnemy( Vector2( 300, 730 ) )
        basicEnemy.debugName = "Steve"
        self.enemies.append( basicEnemy )
        patrollingEnemy = PatrollingEnemy( Vector2( 600, 680 ), [ Vector2( 600, 680 ), Vector2( 800, 680 ) ] )
        patrollingEnemy.debugName = "Wanda"
        self.enemies.append( patrollingEnemy )
        
        
        
        
        
        
        
        
        
        