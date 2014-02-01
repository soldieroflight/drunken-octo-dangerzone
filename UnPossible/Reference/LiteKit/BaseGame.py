import pygame

from LiteKit.EventManager import ObjectEventManager

class BaseGame(object):
    def __init__(self, **kwargs):
        pygame.init()

        self.state = "SETUP"
        
        self.displayWidth = kwargs.get("width", 1024)
        self.displayHeight = kwargs.get("height", 768)
        self.displaybgColor = kwargs.get("bgColor", (0, 0, 0))
        
        self.screen = pygame.display.set_mode((self.displayWidth, self.displayHeight))
        
        self.framerateCap = 30
        
        self.eventManager = ObjectEventManager()
        
        self.clock = pygame.time.Clock()
        
        self.eventManager.registerListener(pygame.QUIT, self.exitButtonPress)
        
    def update(self):
        self.eventManager.processEvents()
        
    def draw(self):
        self.screen.fill(self.displaybgColor)
    
    def exitButtonPress(self, event):
        self.quit()
    
    def quit(self):
        self.state = "QUIT"
        
    def run(self):
        while self.state != "QUIT":
            self.update()
            self.draw()
            self.clock.tick(self.framerateCap)
            pygame.display.flip()
            
def testFunc(event):
    print(event.pos)
    
if __name__ == "__main__":
    exampleGame = BaseGame(bgColor=(155, 155, 155))
    exampleGame.eventManager.registerListener(pygame.MOUSEBUTTONDOWN, testFunc)

    exampleGame.run()