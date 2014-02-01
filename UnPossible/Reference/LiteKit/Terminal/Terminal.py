class LiteTerminal(object):
    def __init__(self):
        self.PROMPT_CHAR = ":"
    
        self.state = "INIT"
        self.commands = {}
        
        self.setupReservedCommands()
        
    def registerCommand(self, commandData):
        pass
        
    def takeInput(self, string):
        arguments = []
        if ' ' in string:
            commandID = string.split()[0]
            arguments = string.split()[1:]
        else:
            commandID = string
        if commandID in self.commands.keys():
            self.commands[commandID](arguments)
    
    def setupReservedCommands(self):
        self.commands["quit"] = self.quit
        self.commands["print"] = self.echo
        
    def displayPrompt(self):
        inputString = raw_input(self.PROMPT_CHAR)
        self.takeInput(inputString)
    
    def echo(self, args):
        print(" ".join(args))
    
    def quit(self, args):
        self.state = "QUIT"
        
if __name__ == "__main__":

    testTerminal = LiteTerminal()
    while testTerminal.state != "QUIT":
        testTerminal.displayPrompt()
