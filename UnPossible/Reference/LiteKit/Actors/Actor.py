class Actor(object):
    def __init__(self, **kwargs):
        self.width = kwargs.get("width", 100)
        self.height = kwargs.get("height", 100)
        self.xPos = kwargs.get("startX", 0)
        self.yPos = kwargs.get("startY", 0)
        self.debugDrawColor = kwargs.get("debugDrawColor", (155, 155, 155))
        
        self.sprite = False
        
    def update(self):
        pass
        
    def draw(self, destSurface):
        if self.sprite:
            pass
            
        else:
            pass
        
    def recieveEvent(self):
        pass
        
