import pygame
from physics.mathutils import *
from animatedObject import *
import random

class BackgroundPlane(object):
    def __init__(self, image):
        self.image = image
        self.dimensions = image.get_size()

    def update(self, deltaTime):
        pass

    def draw(self, screen, subrect):
        screen.blit(self.image, (0, 0), subrect)

class AnimatedBackgroundPlane(object):
    def __init__(self, animation):
        self.animation = animation
        self.dimensions = animation.rect.size

    def update(self, deltaTime):
        self.animation.update(deltaTime)

    def draw(self, screen, subrect):
        self.animation.draw(screen, (0, 0), subrect=subrect)

class BackgroundSprite(object):
    def __init__(self, animation, parallaxDimensions=None, parallaxQuantity=None, worldDimensions=None, worldCoordinates=None, parallaxCoordinates=None):
        self.animation = animation
        if parallaxDimensions != None:
            self.dimensions = parallaxDimensions
        elif parallaxQuantity != None and worldDimensions != None:
            assert parallaxQuantity < 1.0
            self.dimensions = (worldDimensions[0] / parallaxQuantity, worldDimensions[1] / parallaxQuantity)
        else:
            assert False
        self.imageDimensions = animation.rect.size

        if parallaxCoordinates != None:
            self.coordinates = parallaxCoordinates
        elif worldCoordinates != None and worldDimensions != None:
            self.coordinates = (worldCoordinates[0] * (float(self.dimensions[0]) / worldDimensions[0]), worldCoordinates[1] * (float(self.dimensions[1]) / worldDimensions[1]))
        else:
            assert False
        assert self.coordinates[0] + self.imageDimensions[0] < self.dimensions[0] and self.coordinates[1] + self.imageDimensions[1] < self.dimensions[1]

    def update(self, deltaTime):
        self.animation.update(deltaTime)

    def draw(self, screen, subrect):
        rect = pygame.Rect(self.coordinates, self.dimensions)
        if not subrect.colliderect(rect):
            return
        coordinates = (self.coordinates[0] - subrect.left, self.coordinates[1] - subrect.top)
        self.animation.draw(screen, coordinates)

class Camera(object):
    """Transforms coordinates from world to screen"""
    def __init__(self, screenSize, worldSize, screen):
        self.rect = pygame.Rect(0, 0, screenSize.x, screenSize.y)
        self.worldSize = worldSize
        self.screen = screen
        self.backgrounds = []

    def set_background(self, surfaces):
        for surface in surfaces:
            assert surface.dimensions[0] <= self.worldSize.x and surface.dimensions[1] <= self.worldSize.y
            assert surface.dimensions[0] >= self.rect.width and surface.dimensions[1] >= self.rect.height
        self.backgrounds = surface

    def debug_set_background(self, dimensionsList, spriteDimensions=None):
        for dimensions in dimensionsList:
            assert dimensions[0] <= self.worldSize.x and dimensions[1] <= self.worldSize.y
            assert dimensions[0] >= self.rect.width and dimensions[1] >= self.rect.height
        self.backgrounds = [BackgroundPlane(pygame.Surface(dimensions, pygame.SRCALPHA)) for dimensions in dimensionsList]
        for background in self.backgrounds:
            for i in range(0, 10):
                dimensions = background.dimensions
                pos = (int(random.uniform(0, dimensions[0])), int(random.uniform(0, dimensions[1])))
                radius = int(random.uniform(1.0, 100.0))
                color = (int(random.uniform(0, 255)), int(random.uniform(0, 255)), int(random.uniform(0, 255)))
                pygame.draw.circle(background.image, color, pos, radius)
        if spriteDimensions != None:
            for dimensions in spriteDimensions:
                assert dimensions[0][0] <= self.worldSize.x and dimensions[0][1] <= self.worldSize.y
                assert dimensions[0][0] >= self.rect.width and dimensions[0][1] >= self.rect.height
            sprites = [BackgroundSprite(FakeAnimatedObject(pygame.Surface(dimensions[1], pygame.SRCALPHA)), parallaxDimensions=dimensions[0], parallaxCoordinates=dimensions[2]) for dimensions in spriteDimensions]
            for sprite in sprites:
                    radius = int(min(sprite.imageDimensions[0] / 2, sprite.imageDimensions[1] / 2))
                    color = (int(random.uniform(0, 255)), int(random.uniform(0, 255)), int(random.uniform(0, 255)))
                    pygame.draw.circle(sprite.animation.image, color, (int(sprite.imageDimensions[0] / 2), int(sprite.imageDimensions[1] / 2)), radius)
            self.backgrounds.extend(sprites)

    def transform(self, worldCoordinates):
        if isinstance(worldCoordinates, Vector2):
            return (worldCoordinates - Vector2(self.rect.x, self.rect.y)).safe_pos()
        elif isinstance(worldCoordinates, pygame.Rect):
            return worldCoordinates.move((-self.rect.x, -self.rect.y))
        else:
            return (int(worldCoordinates[0] - self.rect.x), int(worldCoordinates[1] - self.rect.y))

    def update(self, playerPos):
        assert isinstance(playerPos, Vector2)
        #if ( playerPos.y > self.rect.height * 0.5 )
        self.rect.bottom = min(self.worldSize.y, playerPos.y + self.rect.height * 0.6)
        self.rect.top = max(0, self.rect.top)
        self.rect.centerx = playerPos.x
        self.rect.right = min(self.worldSize.x, self.rect.right)
        self.rect.left = max(0, self.rect.left)

    def isInCamera(self, boundingBox):
        assert isinstance(boundingBox, pygame.Rect)
        return self.rect.colliderect(boundingBox)

    def updateBackground(self, deltaTime):
        for background in self.backgrounds:
            background.update(deltaTime)

    def drawBackground(self):
        backgroundRect = self.rect.copy()
        width = self.worldSize.x - self.rect.width
        height = self.worldSize.y - self.rect.height
        for background in self.backgrounds:
            dimensions = background.dimensions
            backgroundRect.left = self.rect.left / width * (dimensions[0] - self.rect.width)
            backgroundRect.top = self.rect.top / height * (dimensions[1] - self.rect.height)
            background.draw(self.screen, backgroundRect)
            #self.screen.blit(background, (0, 0), backgroundRect)
        pass

    def blit(self, source, worldCoords, area=None, special_flags = 0):
        if isinstance(worldCoords, pygame.Rect):
            if not self.isInCamera(worldCoords):
                return
        else:
            worldRect = pygame.Rect(worldCoords, area.size)
            if not self.isInCamera(worldRect):
                return
        screenCoords = self.transform(worldCoords)
        self.screen.blit(source, screenCoords, area, special_flags)

    def line(self, color, start_pos, end_pos, width=1):
        worldRect = pygame.Rect(min(start_pos[0], end_pos[0]), min(start_pos[1], end_pos[1]), 0, 0)
        worldRect.width = max(start_pos[0], end_pos[0]) - worldRect.left
        worldRect.height = max(start_pos[1], end_pos[1]) - worldRect.top
        if not self.isInCamera(worldRect):
            return
        transformedStart = self.transform(start_pos)
        transformedEnd = self.transform(end_pos)
        pygame.draw.line(self.screen, color, transformedStart, transformedEnd, width)

    def lines(self, color, closed, pointlist, width=1):
        left = pointlist[0][0]; top = pointlist[0][1]; right = left; bottom = top
        transformedPoints = []
        for point in pointlist:
            left = min(left, point[0])
            right = max(right, point[0])
            top = min(top, point[1])
            bottom = max(bottom, point[1])
            transformedPoints.append(self.transform(point))
        if not self.isInCamera(pygame.Rect(left, top, right - left, bottom - top)):
            return
        pygame.draw.lines(self.screen, color, closed, transformedPoints, width)

    def circle(self, color, pos, radius, width=0):
        worldRect = pygame.Rect(pos[0] - radius, pos[1] - radius, radius * 2, radius * 2)
        if not self.isInCamera(worldRect):
            return
        pygame.draw.circle(self.screen, color, self.transform(pos), radius, width)

    def polygon(self, color, pointlist, width=0):
        left = pointlist[0][0]; top = pointlist[0][1]; right = left; bottom = top
        transformedPoints = []
        for point in pointlist:
            left = min(left, point[0])
            right = max(right, point[0])
            top = min(top, point[1])
            bottom = max(bottom, point[1])
            transformedPoints.append(self.transform(point))
        if not self.isInCamera(pygame.Rect(left, top, right - left, bottom - top)):
            return
        pygame.draw.polygon(self.screen, color, transformedPoints, width)
