from baseobjects import *

class Platform(PhysicalObject):
    def __init__(self, topLeftPos=None, width=0, height=0, centerPos=None):
        
        
        if ( centerPos == None ):
            super().__init__(topLeftPos)
            
            convertedPos = Vector2( topLeftPos.x + width / 2, topLeftPos.y + height / 2 )
            
            #KEVIN MAKE ME BETTER PLEASE
            guiltyHackPos = Vector2( convertedPos.x, 900 - convertedPos.y )
            
            self.rigidbody = AABB(guiltyHackPos, width, height)
        
        else:
            super().__init__(centerPos)
            self.rigidbody = AABB(centerPos, width, height)
        
        self.rigidbody.owner = self
        self.rigidbody.useDynamics = False
        
    def debug_draw(self, camera):
        self.rigidbody.draw(camera)

class TimeBubble(PhysicalObject):
    def __init__(self, timeScale, pos, radius, lifetime=0.0):
        super().__init__(pos)
        self.timeScale = timeScale
        self.rigidbody = Sphere(pos, radius)
        self.rigidbody.solid = False
        self.radius = radius
        self.lifetime = lifetime
        self.dead = False

    def update(self, deltaTime):
        if self.lifetime > 0:
            self.lifetime -= deltaTime
            if self.lifetime <= 0:
                self.dead = True #external cleanup

    def contains(self, pos):
        return dist(self.rigidbody.position, pos) < self.radius

    def debug_draw(self, camera):
        self.rigidbody.draw(camera)

class TimeProjectile(Projectile):
    def __init__(self, game, timeScale, pos, dir, radius):
        super().__init__(pos, dir)
        self.bubble = TimeBubble(timeScale, pos, radius, 20.0)
        game.timeBubbles.append(self.bubble)

    def sync_transform(self):
        super().sync_transform()
        self.bubble.rigidbody.position = self.rigidbody.position