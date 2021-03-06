import pygame
from physics.mathutils import *

colorKey = (255, 255, 0)
bwColorKey = (127, 127, 127)

class AnimatedObject(object):
    def __init__(self, colorFilename, numSpriteRows, numSpriteCols, colorKey=None):
        if colorKey != None:
            self.colorImage = pygame.image.load(colorFilename).convert()
            self.colorImage.set_colorkey(colorKey)
        else:
            self.colorImage = pygame.image.load(colorFilename).convert_alpha()
        
        self.numSpriteRows = numSpriteRows
        self.numSpriteCols = numSpriteCols
        self.currentFrame = 0
        self.animationStartFrame = 0
        self.animationEndFrame = 0
        self.animationSpeed = 1 #1 frame per second
        self.animationTime = 0
        self.animationLoop = False
        
        self.size = (self.colorImage.get_size()[0] / numSpriteCols, self.colorImage.get_size()[1] / numSpriteRows)
        self.rect = pygame.Rect((0, 0), self.size)
        self.animating = False
        
    def animate(self, startFrame, endFrame, speed=1, loop=False):
        """Sets up an animation loop from startFrame to endFrame at speed frames/second"""
        self.animating = True
        self.animationStartFrame = startFrame
        self.currentFrame = startFrame
        self.animationEndFrame = endFrame
        self.animationSpeed = float(speed)
        self.animationLoop = loop
        
    def stop(self):
        self.animating = False
        self.animationLoop = False
        
    def update(self, deltaTime):
        """Updates the sprite to use a different sprite from the sheet, based on the current animation data"""
        if not self.animating: return
        self.animationTime += deltaTime
        self.currentFrame += int(self.animationTime * self.animationSpeed)
        self.animationTime %= (1.0/self.animationSpeed)
        if self.animationLoop:
            self.currentFrame = ((self.currentFrame - self.animationStartFrame) % (self.animationEndFrame - self.animationStartFrame + 1)) + self.animationStartFrame
        elif self.currentFrame >= self.animationEndFrame:
            self.currentFrame = self.animationEndFrame
            self.animating = False
        
    def draw(self, screen, pos=None, anchor=None, subrect=None):
        spriteRow = int(self.currentFrame / self.numSpriteCols)
        spriteCol = self.currentFrame % self.numSpriteCols
        area = pygame.Rect((self.rect.width * spriteCol, self.rect.height * spriteRow), self.size)
        
        if pos != None:
            if isinstance(pos, Vector2):
                pos = pos.safe_pos()
            if anchor == 'center' or anchor == None:
                self.rect.center = pos
            elif anchor == 'bottom':
                self.rect.midbottom = pos
            elif anchor == 'top':
                self.rect.midtop = pos
            else:
                self.rect.center = (pos[0] + anchor[0], pos[1] + anchor[1])

        if subrect != None:
            area = pygame.Rect((area.left + subrect.left, area.top + subrect.top), subrect.size)
        
        screen.blit(self.colorImage, self.rect.topleft, area)

class FakeAnimatedObject(object):
    def __init__(self, image):
        self.image = image
        self.size = self.image.get_size()
        self.rect = pygame.Rect((0, 0), self.size)

    def animate(self, startFrame, endFrame, speed=1, loop=False):
        pass

    def stop(self):
        pass

    def update(self, deltaTime):
        pass

    def draw(self, screen, pos=None, anchor=None, subrect=None):
        if subrect is None:
            subrect = pygame.Rect((0, 0), self.size)
        
        if pos != None:
            if isinstance(pos, Vector2):
                pos = pos.safe_pos()
            if anchor == 'center' or anchor == None:
                self.rect.center = pos
            elif anchor == 'bottom':
                self.rect.midbottom = pos
            elif anchor == 'top':
                self.rect.midtop = pos
            else:
                self.rect.center = (pos[0] + anchor[0], pos[1] + anchor[1])
        
        screen.blit(self.image, self.rect.topleft, subrect)