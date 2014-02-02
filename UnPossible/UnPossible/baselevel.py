from physics.mathutils import *

class Level(object):
    def __init__(self):
        # This is the size of the world, in pixels.
        self.worldSize = Vector2(0, 0)
        
        # This is the y-value of the lowest ground.
        self.ground = 0
        
        # This is the starting position of the player.
        self.playerStart = Vector2(0, 0)
        
        # All of the platforms present in the world.
        self.platforms = []
        
        # All of the switches present in the world.
        self.switches = []
        
        # All of the enemies in the world.
        self.enemies = []
        
        # TODO: Scheme for scenery?
        
    def load(self):
        # Here goes all the code which creates the platforms, switches, links,
        # and enemies that are present in the level.
        # These objects must be placed into their respective buckets in order
        # for the main game logic to access them.
        pass
        