import pygame
from .endpoint import *
from physics import particles, mathutils
from physics.mathutils import Vector2

class Link(Endpoint):
    """Connects a trigger to an endpoint"""
    def __init__(self, targets, path, activationTime):
        """Initialize with a set of components to activate, a list of points for the path, and seconds for activation"""
        super().__init__()
        self.targets = targets
        self.path = path
        self.progress = 0.0
        self.activationTime = activationTime
        self.active = False
        self.particles = particles.ParticleEmitter(self.path[0], {'emitterArea': 0,
                                                                  'minEmitRate': 10,
                                                                  'maxEmitRate': 20,
                                                                  'randomVelocity': Vector2(2, 2),
                                                                  'minOutwardVelocity': 5,
                                                                  'maxOutwardVelocity': 10
                                                                  })
        self.particles.pause()

    def activate(self):
        """Activated: begin countdown"""
        if self.active:
            return
        self.active = True
        self.progress = 0.0
        self.particles.unpause()

    def getActivationPoint(self):
        if not self.active:
            return self.path[0]
        pairs = []
        lastPoint = None
        totalLength = 0.0
        for point in self.path:
            if lastPoint != None:
                pairs.append((lastPoint, point))
                totalLength += mathutils.dist(lastPoint, point)
            lastPoint = point

        drawnLength = 0
        for pair in pairs:
            thisLength = mathutils.dist(pair[0], pair[1])
            if thisLength + drawnLength > totalLength * self.progress:
                toDraw = (totalLength * self.progress - drawnLength)
                endpoint = pair[0] + (pair[1] - pair[0]).normal().scale(toDraw)
                return endpoint
            else:
                drawnLength += thisLength
        return self.path[-1]

    def update(self, deltaTime, timeBubbles):
        if self.active:
            activationPoint = self.getActivationPoint()
            self.particles.pos = activationPoint

            timeScale = 1.0
            for bubble in timeBubbles:
                if bubble.contains(activationPoint):
                    timeScale *= bubble.timeScale

            self.progress += (deltaTime / self.activationTime * timeScale)
            if self.progress >= 1.0:
                self.reset()
                for target in self.targets:
                    target.trigger()
        self.particles.update(deltaTime, timeBubbles)

    def reset(self):
        """Automatically resets itself after activation"""
        super().reset()
        self.active = False
        self.progress = 0.0
        self.particles.pause()

    def draw(self, camera):
        pairs = []
        lastPoint = None
        totalLength = 0.0
        for point in self.path:
            if lastPoint != None:
                pairs.append((lastPoint, point))
                totalLength += mathutils.dist(lastPoint, point)
            lastPoint = point

        drawnLength = 0
        for pair in pairs:
            camera.line((0, 255, 0), (pair[0].x, pair[0].y), (pair[1].x, pair[1].y))

        for pair in pairs:
            thisLength = mathutils.dist(pair[0], pair[1])
            if thisLength + drawnLength > totalLength * self.progress:
                toDraw = (totalLength * self.progress - drawnLength)
                endpoint = pair[0] + (pair[1] - pair[0]).normal().scale(toDraw)
                camera.line((255, 0, 0), (pair[0].x, pair[0].y), (endpoint.x, endpoint.y))
                break
            else:
                camera.line((255, 0, 0), (pair[0].x, pair[0].y), (pair[1].x, pair[1].y))
                drawnLength += thisLength

        self.particles.draw(camera)