import pygame
from physics.mathutils import *

class Camera(object):
    """Transforms coordinates from world to screen"""
    def __init__(self, screenSize, worldSize, screen):
        self.rect = pygame.Rect(0, 0, screenSize.x, screenSize.y)
        self.worldSize = worldSize
        self.screen = screen

    def transform(self, worldCoordinates):
        if isinstance(worldCoordinates, Vector2):
            return worldCoordinates - Vector2(self.rect.x, self.rect.y)
        elif isinstance(worldCoordinates, pygame.Rect):
            return worldCoordinates.move((-self.rect.x, -self.rect.y))
        else:
            return (worldCoordinates[0] - self.rect.x, worldCoordinates[1] - self.rect.y)

    def update(self, playerPos):
        assert isinstance(playerPos, Vector2)
        self.rect.bottom = min(self.worldSize.y, playerPos.y + self.rect.height / 3.0)
        self.rect.centerx = playerPos.x
        self.rect.right = min(self.worldSize.x, self.rect.right)
        self.rect.left = max(0, self.rect.left)

    def isInCamera(self, boundingBox):
        assert isinstance(boundingBox, pygame.Rect)
        return self.rect.colliderect(boundingBox)

    def blit(self, source, worldCoords, area=None, special_flags = 0):
        assert isinstance(worldCoords, pygame.Rect)
        if not self.isInCamera(worldCoords):
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
