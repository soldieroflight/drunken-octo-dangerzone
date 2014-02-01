import pygame

from Actor import Actor

class ScreenLayer(Actor):
    #TODO: Make these keyword args
    def __init__(self, dimensions=(100, 100), startPos=(0,0), debugDrawColor=(155, 155, 155)):
        self.width = dimensions[0]
        self.height = dimensions[1]
        self.xPos = startPos[0]
        self.yPos = startPos[1]
        self.children = []
        
        self.surface = pygame.Surface(self.width, self.height)
        
    def update(self, destSurface):
        for child in self.children:
            pass