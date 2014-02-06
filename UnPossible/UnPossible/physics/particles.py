import pygame
from .mathutils import *
import math
import random

#How to use:
#ParticleEmitter's constructor takes 2 arguments: a position as a Vector2, and a description as a dictionary
#The dictionary has lots of options to configure the emitter, and if a variable isn't specified, it will use its default
#
#Per emitter:
#    Setting the emitter's lifetime is done through these 3 variables:
#    emitterMinLifetime = 0
#    emitterMaxLifetime = 0
#    lifetimeType = 'forever'
#    The lifetimeType can be either 'forever', 'particles', or 'seconds'
#
#    emitterArea = 1 is the radius of the particle spawning area
#    emitterRange = 0 is the outward percentage of the radius to use: 0 means use everything, 1 means spawn on the rim, 0.5 is spawn in the outer half of the ring
#    colors = [(255, 0, 0)] is a tuple of RGB and will be used to draw a circle if no image is given
#    image = None is a filename to load
#    movementFrame = 'independent'
#    The movementFrame can be either 'independent' (particles use world coordinates), 'inherited' (particles inherit velocity), or 'attached' (particles use emitter frame)
#
#Per emitter per second:
#    minEmitRate = 1 and maxEmitRate = 1 is how many particles per second
#
#Per particle:
#    minSize = 2 and maxSize = 2, in pixels
#    minLifetime = 5 and maxLifetime = 5, in seconds
#    velocity = Vector2(0, 0), in pixels/second
#    randomVelocity = Vector2(0, 0), in pixels/second (automatically uses +/- values)
#    minOutwardVelocity = 0 and maxOutwardVelocity = 0, in pixels (negative for inward)
#
#Per particle per second:
#    force = Vector2(0, 0), in pixels/second^2
#    randomForce = Vector2(0, 0) (calculated every frame) in pixels/second^2
#    damping = 1 should be calculated per second, but is calculated per frame
#        1 damping means don't do anything, > 1 is speed up (increase energy), < 1 is decrease energy (don't use negatives)

class Particle(object):
    def __init__(self, emitter, pos, color, size, vel, force, randForce, damping, lifetime, sizeChange, image, movementFrame, inheritance):
        self.emitter = emitter
        self.pos = pos
        self.color = color
        self.size = size
        self.vel = vel
        self.force = force
        self.randForce = randForce
        self.damping = damping
        self.lifetime = lifetime
        self.sizeChange = sizeChange
        self.image = image
        self.scaledImage = image
        self.attached = (movementFrame == 'attached')

        if movementFrame == 'inherited':
            self.vel += emitter.vel.scale(inheritance)
        
        self.lastSize = 0
        
        self.dead = False
        self.currentLifetime = 0
        
    def update(self, time, timeBubbles):
        if self.dead:
            return
        
        pos = self.pos
        if self.attached:
            pos += self.emitter.pos
        for bubble in timeBubbles:
            if bubble.contains(pos):
                time *= bubble.timeScale

        self.currentLifetime += time
        if self.currentLifetime > self.lifetime:
            self.dead = True
            return
        
        forces = Vector2(self.force.x + random.uniform(-self.randForce.x, self.randForce.x), self.force.y + random.uniform(-self.randForce.y, self.randForce.y))
        forces = forces.scale(time)
        self.vel += forces
        self.vel = self.vel.scale(self.damping ** time)
        self.pos += self.vel.scale(time)
        self.size += self.sizeChange * time
        
        self.dead = self.size <= 0
        
    def draw(self, camera):
        pos = self.pos
        if self.attached:
            pos += self.emitter.pos
        if self.image:
            if self.size != self.lastSize:
                self.scaledImage = pygame.transform.scale(self.image, (int(self.size), int(self.size)))
                self.lastSize = self.size
            camera.blit(self.scaledImage, pygame.Rect(pos.x, pos.y, self.size, self.size))
        else:
            camera.circle(self.color, (int(pos.x), int(pos.y)), int(self.size))
        
class ParticleEmitter(object):
    def __init__(self, pos, description):
        self.particles = []
        self.pos = pos
        
        self.totalEmittedCount = 0
        self.totalEmittedTime = 0
        self.emissionCounter = 0
        self.paused = False
        self.vel = 0
        self.lastPos = pos
        
        if 'minSize' in description:
            self.minSize = description['minSize']
        else:
            self.minSize = 2
        if 'maxSize' in description:
            self.maxSize = description['maxSize']
        else:
            self.maxSize = 2
        
        if 'sizeChange' in description:
            self.sizeChange = description['sizeChange']
        else:
            self.sizeChange = 0
        
        if 'minLifetime' in description:
            self.minLifetime = description['minLifetime']
        else:
            self.minLifetime = 5
        if 'maxLifetime' in description:
            self.maxLifetime = description['maxLifetime']
        else:
            self.maxLifetime = 5
        
        if 'minEmitRate' in description:
            self.minEmitRate = description['minEmitRate']
        else:
            self.minEmitRate = 1
        if 'maxEmitRate' in description:
            self.maxEmitRate = description['maxEmitRate']
        else:
            self.maxEmitRate = 1
        
        if 'lifetimeType' in description:
            self.lifetimeType = description['lifetimeType']
        else:
            self.lifetimeType = 'forever'

        if 'movementFrame' in description:
            self.movementFrame = description['movementFrame']
        else:
            self.movementFrame = 'independent'

        if 'inheritance' in description:
            self.inheritance = description['inheritance']
        else:
            self.inheritance = 1.0

        if 'emitterMinLifetime' in description:
            self.emitterMinLifetime = description['emitterMinLifetime']
        else:
            self.emitterMinLifetime = 0
        if 'emitterMaxLifetime' in description:
            self.emitterMaxLifetime = description['emitterMaxLifetime']
        else:
            self.emitterMaxLifetime = 0
        
        if 'velocity' in description:
            self.velocity = description['velocity']
        else:
            self.velocity = Vector2(0, 0)
        if 'randomVelocity' in description:
            self.randomVelocity = description['randomVelocity']
        else:
            self.randomVelocity = Vector2(0, 0)
        if 'minOutwardVelocity' in description:
            self.minOutwardVelocity = description['minOutwardVelocity']
        else:
            self.minOutwardVelocity = 0
        if 'maxOutwardVelocity' in description:
            self.maxOutwardVelocity = description['maxOutwardVelocity']
        else:
            self.maxOutwardVelocity = 0
            
        if 'emitterArea' in description:
            self.emitterArea = description['emitterArea']
        else:
            self.emitterArea = 1
        if 'emitterRange' in description:
            self.emitterRange = description['emitterRange']
        else:
            self.emitterRange = 0
            
        if 'force' in description:
            self.force = description['force']
        else:
            self.force = Vector2(0, 0)
        if 'randomForce' in description:
            self.randomForce = description['randomForce']
        else:
            self.randomForce = Vector2(0, 0)
            
        if 'damping' in description:
            self.damping = description['damping']
        else:
            self.damping = 1
            
        if 'image' in description:
            self.images = [pygame.image.load(description['image']).convert_alpha()]
        elif 'images' in description:
            self.images = [pygame.image.load(x).convert_alpha() for x in description['images']]
        else:
            self.images = [None]
        if 'color' in description:
            self.colors = [description['color']]
        elif 'colors' in description:
            self.colors = description['colors']
        else:
            self.colors = [(255, 0, 0)]
            
        self.emitterStopValue = random.uniform(self.emitterMinLifetime, self.emitterMaxLifetime)
        
    def isEmitting(self):
        if self.paused:
            return False
        if self.lifetimeType == 'forever':
            return True;
        elif self.lifetimeType == 'particles':
            return self.totalEmittedCount < self.emitterStopValue
        else:
            return self.totalEmittedTime < self.emitterStopValue
        
    def isAlive(self):
        if self.isEmitting() or self.paused:
            return True
        else:
            return len(self.particles) > 0
            
    def stop(self):
        self.emitterStopValue = -1
        self.lifetimeType = 'seconds'

    def pause(self):
        self.paused = True

    def unpause(self):
        self.paused = False
                
    def emit(self):
        posScale = 1 - random.uniform(0, 1 - self.emitterRange)
        
        scaledSize = self.emitterArea * posScale
        theta = random.uniform(0, 2 * math.pi)
        pos = Vector2(math.cos(theta), math.sin(theta)).scale(scaledSize)
        posNormalized = pos.normal()
        if self.movementFrame != 'attached':
            pos += self.pos
        
        vel = self.velocity + \
            self.randomVelocity.scale(Vector2(random.uniform(-1, 1), random.uniform(-1, 1))) + \
            posNormalized.scale(random.uniform(self.minOutwardVelocity, self.maxOutwardVelocity))
        
        lifetime = random.uniform(self.minLifetime, self.maxLifetime)
        size = random.uniform(self.minSize, self.maxSize)
        self.particles.append(Particle(self, pos, random.choice(self.colors), size, vel, self.force, self.randomForce, self.damping, lifetime, self.sizeChange, random.choice(self.images), self.movementFrame, self.inheritance))
            
    def update(self, time, timeBubbles):
        for particle in self.particles:
            particle.update(time, timeBubbles)
            if particle.dead:
                self.particles.remove(particle)

        self.vel = (self.pos - self.lastPos).scale(1/time)
        self.lastPos = self.pos
                
        if self.isEmitting():
            for bubble in timeBubbles:
                if bubble.contains(self.pos):
                    time *= bubble.timeScale

            self.totalEmittedTime += time
            self.emissionCounter += random.uniform(self.minEmitRate, self.maxEmitRate) * time
            numNewParticles = int(self.emissionCounter)
            
            while self.emissionCounter >= 1 and self.isEmitting():
                self.emit()
                self.emissionCounter -= 1
                self.totalEmittedCount += 1
                
    def draw(self, camera):
        for particle in self.particles:
            particle.draw(camera)
            
class SurfaceShatterParticles(ParticleEmitter):
    def __init__(self, surface, position, description):
        ParticleEmitter.__init__(self, position, description)
        
        rect = surface.get_rect()
        center = Vector2(rect.centerx, rect.centery)
        imageDims = rect.width
        if rect.height > rect.width:
            imageDims = rect.height
        
        size = self.minSize
        surfArray = pygame.surfarray.array3d(surface)

        surfs = []
        positions = []
        for i in range(0,len(surfArray),size):
            for j in range(0,len(surfArray[i]),size):
                surfs.append(surface.subsurface(pygame.Rect(i,j,size,size,)))
                positions.append(Vector2(i+1,j+1))
                
        for i in range(len(surfs)):
            vel = self.velocity + \
                self.randomVelocity.scale(Vector2(random.uniform(-1, 1), random.uniform(-1, 1))) + \
                (positions[i] - center).scale(random.uniform(self.minOutwardVelocity, self.maxOutwardVelocity) / (imageDims / 2))
            
            lifetime = random.uniform(self.minLifetime, self.maxLifetime)
            
            pos = positions[i] + position
            self.particles.append(Particle(self, pos, (0,0,0), size, vel, self.force, self.randomForce, self.damping, lifetime, self.sizeChange, surfs[i], self.movementFrame, 1.0))
            
        self.stop()
        self.exploded = False
        
    def start(self):
        self.exploded = True
        
    def update(self, dt):
        if not self.exploded: return
        ParticleEmitter.update(self, dt, [])
            
            
if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    #FIREWORKS
    emitterDesc = {'emitterArea': 10, 'emitterRange': 0, 'minSize': 3, 'maxSize': 10, 'minLifetime': 1, 'maxLifetime': 3, 'minEmitRate': 100, 'maxEmitRate': 500}
    emitterDesc['randomVelocity'] = Vector2(10, 10)
    emitterDesc['velocity'] = Vector2(0, -100)
    emitterDesc['minOutwardVelocity'] = 30
    emitterDesc['maxOutwardVelocity'] = 10
    #emitterDesc['image'] = 'particle.png'
    emitterDesc['colors'] = [(255, 0, 0), (255, 255, 0), (0, 255, 0), (0, 0, 255), (255, 0, 255), (255, 255, 255), (0, 255, 255)]
    #emitterDesc['sizeChange'] = 5
    emitterDesc['lifetimeType'] = 'particles'
    emitterDesc['emitterMinLifetime'] = 100
    emitterDesc['emitterMaxLifetime'] = 200
    emitterDesc['force'] = Vector2(0, 100)
    #emitterDesc['randomForce'] = Vector2(1000, 1000)
    emitterDesc['damping'] = 1.02

    emitters = []

    while 1:
        clock.tick(30)
        screen.fill((0, 0, 0))
        
        for emitter in emitters:
            emitter.update(1.0/30)
            emitter.draw(screen)
            
        if random.random() < 0.05:
            emitters.append(ParticleEmitter(Vector2(random.uniform(0, 800), random.uniform(0, 600)), emitterDesc))
        
        pygame.event.pump()
        
        pygame.display.flip()