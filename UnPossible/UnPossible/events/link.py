import pygame
from .endpoint import *
from physics import particles, mathutils
from physics.mathutils import Vector2

class link(endpoint):
    """Connects a trigger to an endpoint"""
    def __init__(self, targets, path, activation_time):
        """Initialize with a set of components to activate, a list of points for the path, and seconds for activation"""
        super().__init__()
        self.targets = targets
        self.path = path
        self.time_modifier = 1.0
        self.progress = 0.0
        self.activation_time = activation_time
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

    def get_activation_point(self):
        if not self.active:
            return self.path[0]
        pairs = []
        last_point = None
        total_length = 0.0
        for point in self.path:
            if last_point != None:
                pairs.append((last_point, point))
                total_length += mathutils.dist(last_point, point)
            last_point = point

        drawn_length = 0
        for pair in pairs:
            this_length = mathutils.dist(pair[0], pair[1])
            if this_length + drawn_length > total_length * self.progress:
                to_draw = (total_length * self.progress - drawn_length)
                endpoint = pair[0] + (pair[1] - pair[0]).normal().scale(to_draw)
                return endpoint
            else:
                drawn_length += this_length
        return self.path[-1]

    def update(self, delta_time):
        if self.active:
            self.progress += (delta_time / self.activation_time * self.time_modifier)
            self.particles.pos = self.get_activation_point()
            if self.progress >= 1.0:
                self.reset()
                for target in self.targets:
                    target.trigger()
        self.particles.update(delta_time)

    def reset(self):
        """Automatically resets itself after activation"""
        super().reset()
        self.active = False
        self.progress = 0.0
        self.particles.pause()

    def set_time_modifier(self, new_time_modifier):
        self.time_modifier = new_time_modifier

    def draw(self, screen):
        pairs = []
        last_point = None
        total_length = 0.0
        for point in self.path:
            if last_point != None:
                pairs.append((last_point, point))
                total_length += mathutils.dist(last_point, point)
            last_point = point

        drawn_length = 0
        for pair in pairs:
            pygame.draw.line(screen, (0, 255, 0), (pair[0].x, pair[0].y), (pair[1].x, pair[1].y))

        for pair in pairs:
            this_length = mathutils.dist(pair[0], pair[1])
            if this_length + drawn_length > total_length * self.progress:
                to_draw = (total_length * self.progress - drawn_length)
                endpoint = pair[0] + (pair[1] - pair[0]).normal().scale(to_draw)
                pygame.draw.line(screen, (255, 0, 0), (pair[0].x, pair[0].y), (endpoint.x, endpoint.y))
                break
            else:
                pygame.draw.line(screen, (255, 0, 0), (pair[0].x, pair[0].y), (pair[1].x, pair[1].y))
                drawn_length += this_length

        self.particles.draw(screen)