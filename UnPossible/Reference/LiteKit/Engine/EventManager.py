import pygame

class ObjectEventManager(object):
    def __init__(self):
        self.listeners = {}
        
        self.recording = False
        
    def processEvents(self):
        '''Processes the events since the last time pygame.event.get() was called. Searched
        the listeners list, and then calls any callback functions associated with that key
        @return     returns the number of events that were handled
        '''
        for event in pygame.event.get():
            if event.type in self.listeners:
                callbackList = self.listeners[event.type]
                for callbackFunc in callbackList:
                    callbackFunc(event)
        
    def registerListener(self, eventID, callbackFunc):
        '''Registers a callback function to be called when an event of type eventID is found
        @param  eventID         The event type to check for
        @param  callbackFunc    The callback function to call when the event is found
        @return success         Returns if the function was already there
        '''
        currentList = self.listeners.get(eventID, [])
        
        #Check if the function is already there
        if callbackFunc in currentList:
            return False
        
        #Else add it as a callback function
        currentList.append(callbackFunc)
        self.listeners[eventID] = currentList
        return True
        
    def removeListener(self, eventID, callbackFunc):
        '''Removes a callback function from when an event of tyoe eventID is found. If that
        function does not exist, do nothing
        @parem  eventID         The event type to check for
        @parem  callbackFunc    The callbak function to remove
        @return success         Returns if the function was removed
        '''
        currentList = self.listeners.get(eventID, [])
        
        #check if the function is in the list
        if callbackFunc in currentList:
            currentList.remove(callbackFunc)
            return True