import pygame

class FramerateMonitor(object):
    def __init__(self, init=30, **kwargs):
        self.bufferSize = kwargs.get('bufferSize', 10)
        self.buffer = [init for x in range(self.bufferSize)]
        self.targetFps = init
        self.targetTime = 1.0 / self.targetFps
        self.averageFps = self.targetFps
        self.averageTime = 1.0 / self.averageFps
        self.writeIndex = 0
        self.frequency = kwargs.get('frequency', 1.0)
        self.localTime = 0.0
        
        # Reporting properties.
        self.reportLocation = (10, 10)
        self.reportSpacing = 20
        self.reportSize = 20
        self.reportColorGood = kwargs.get('reportColorGood', (50,220,50))
        self.reportColorBad = kwargs.get('reportColorBad', (220,50,50))
        self.font = pygame.font.Font(None,20)
        self.reportFramerate = kwargs.get('reportFramerate', True)
        self.reportFrametime = kwargs.get('reportFrametime', True)
        
    def update(self, deltaTime):
        self.buffer[self.writeIndex] = deltaTime
        self.writeIndex += 1
        if self.writeIndex >= self.bufferSize:
            self.writeIndex = 0
        
        self.localTime += deltaTime
        if self.localTime > self.frequency:
            self.localTime -= self.frequency
            self.averageTime = sum(self.buffer) / self.bufferSize
            self.averageFps = 1.0 / self.averageTime
            
    def draw(self, screen):
        currentx = self.reportLocation[0]
        currenty = self.reportLocation[1]
        if self.reportFramerate:
            color = self.reportColorGood if self.averageFps > self.targetFps else self.reportColorBad
            fps = self.font.render("Framerate: %.3f" % self.averageFps, 1, color)
            fpsRect = fps.get_rect()
            fpsRect.topleft = (currentx, currenty)
            screen.blit(fps, fpsRect)
            currenty += self.reportSpacing
        if self.reportFrametime:
            color = self.reportColorGood if self.averageTime < self.targetTime else self.reportColorBad
            fps = self.font.render("Frametime: %.3f" % self.averageTime, 1, color)
            fpsRect = fps.get_rect()
            fpsRect.topleft = (currentx, currenty)
            screen.blit(fps, fpsRect)
            currenty += self.reportSpacing