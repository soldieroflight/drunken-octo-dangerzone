from physics.mathutils import *
from baselevel import *
from levelobjects import *
from player import *

class Game(object):
    def __init__(self, screen):
        self.projectiles = []
        self.planes = []
        self.solids = []
        self.platforms = []
        self.enemies = []
        self.switches = []
        self.updatable = []
        self.everything = []
        self.player = None
        self.screen = screen

    def load_level(self, level):
        assert isinstance(level, Level)
        self.level = level
    
        # Make the boundaries of the level.
        # Ground.
        self.planes.append(Plane(Vector2(0, level.ground), Vector2(0.0, -1.0)))
        # Left bound.
        self.planes.append(Plane(Vector2(0, 0), Vector2(1.0, 0.0)))
        # Right bound.
        self.planes.append(Plane(Vector2(level.worldSize.x, 0), Vector2(-1.0, 0.0)))
        # Ceiling.
        self.planes.append(Plane(Vector2(0, 0), Vector2(0.0, 1.0)))
    
        # Now let the level do its thing.
        level.load()
    
        self.player = Player(level.playerStart)
        self.camera = Camera(Vector2(640, 480), self.level.worldSize, self.screen)
    
        self.enemies.extend(level.enemies)
        self.switches.extend(level.switches)
        self.platforms.extend(level.platforms)
        self.solids.extend(self.enemies)
        self.solids.extend(self.planes)
        self.solids.extend(self.platforms)
        self.updatable.extend(self.enemies)
        self.updatable.extend(self.platforms)
        self.updatable.append(self.player)

        self.everything.extend(self.solids)
        self.everything.extend(self.switches)
        self.everything.append(self.player)

    def update(self, deltaTime):
        for obj in self.updatable:
            obj.update(deltaTime)
        for proj in self.projectiles:
            proj.update(deltaTime)

        for obj in self.solids:
            test_collision(self.player.rigidbody, obj.rigidbody)
            for proj in self.projectiles:
                test_collision(proj.rigidbody, obj.rigidbody)
                if proj.expired:
                    self.projectiles.remove(proj)
                    del proj
        
        for obj in self.updatable:
            obj.sync_transform()

        self.camera.update(self.player.rigidbody.position)

    def draw(self):
        for obj in self.everything:
            obj.debug_draw(self.camera)
        
        for proj in self.projectiles:
            proj.debug_draw(self.camera)