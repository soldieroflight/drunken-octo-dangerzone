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
        self.links = []
        self.updatable = []
        self.everything = []
        self.timeBubbles = []
        self.particles = []
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
    
        self.player = Player(self, level.playerStart)
        self.camera = Camera(Vector2(640, 480), self.level.worldSize, self.screen)
    
        self.enemies.extend(level.enemies)
        self.switches.extend(level.switches)
        self.links.extend(level.links)
        self.platforms.extend(level.platforms)
        # Solids are anything that collides.
        self.solids.extend(self.enemies)
        self.solids.extend(self.planes)
        self.solids.extend(self.platforms)
        # Updatables are any GameObjects.
        self.updatable.extend(self.enemies)
        self.updatable.extend(self.platforms)
        self.updatable.append(self.player)
        self.updatable.extend(self.switches)
        self.updatable.extend(self.links)

        self.particles.extend([x.particles for x in self.links])

        self.everything.extend(self.solids)
        self.everything.append(self.player)
        self.everything.extend(self.switches)
        self.everything.extend(self.links)
        self.everything.extend(self.timeBubbles)

    def update(self, deltaTime):
        # Update pass.
        for obj in self.updatable:
            localTime = deltaTime
            for bubble in self.timeBubbles:
                if test_collision(obj.rigidbody, bubble.rigidbody):
                    localTime *= bubble.timeScale
            obj.update(localTime)
        for proj in self.projectiles:
            localTime = deltaTime
            for bubble in self.timeBubbles:
                if test_collision(proj.rigidbody, bubble.rigidbody):
                    localTime *= bubble.timeScale
            proj.update(localTime)

        # Particle update.
        for particles in self.particles:
            particles.update(deltaTime, self.timeBubbles)
            if not particles.isAlive():
                self.particles.remove(particles)

        # Collision pass.
        for obj in self.solids:
            test_collision(self.player.rigidbody, obj.rigidbody)
            for proj in self.projectiles:
                test_collision(proj.rigidbody, obj.rigidbody)
                if proj.expired:
                    self.projectiles.remove(proj)
                    del proj

        for obj in self.switches:
            test_collision(self.player.rigidbody, obj.rigidbody)
        
        # Post-update cleanup.
        for obj in self.updatable:
            obj.sync_transform()
        for proj in self.projectiles:
            proj.sync_transform()

        # Camera pass.
        self.camera.update(self.player.rigidbody.position)

    def draw(self):
        self.camera.drawBackground()

        for obj in self.everything:
            obj.debug_draw(self.camera)
        
        for proj in self.projectiles:
            proj.debug_draw(self.camera)

        for particles in self.particles:
            particles.draw(self.camera)

        for bubble in self.timeBubbles:
            bubble.debug_draw(self.camera)