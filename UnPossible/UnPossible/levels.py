from kevinland import *
from baselevel import *

# This is a sample level.
class TestLevel(Level):
    def __init__(self):
        super().__init__()
        self.worldSize = (800, 600)
        self.ground = 500
        self.playerStart = (100, 400)
        
    def load(self):
        super().load()
        
        platforms.append(Platform(Vector2(200, 330), 100, 10))
        platforms.append(Platform(Vector2(300, 280), 100, 10))