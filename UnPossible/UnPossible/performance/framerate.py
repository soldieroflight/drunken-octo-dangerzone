class FramerateMonitor(object):
    def __init__(self, init=30, freq=1.0, bufferSize=10):
        self.bufferSize = bufferSize
        self.buffer = [init for x in range(bufferSize)]
        self.average = init
        self.writeIndex = 0
        self.frequency = 1.0
        self.localTime = 0.0
        
    def update(self, deltaTime):
        self.buffer[self.writeIndex] = deltaTime
        self.writeIndex += 1
        if self.writeIndex >= self.bufferSize:
            self.writeIndex = 0
        
        self.localTime += deltaTime
        if self.localTime > self.frequency:
            self.localTime -= self.frequency
            self.average = 1.0 / (sum(self.buffer) / self.bufferSize)
            