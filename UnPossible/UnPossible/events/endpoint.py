class Endpoint(object):
    """Receives events from triggers"""
    def __init__(self):
        self.triggered = False

    def trigger(self):
        """Occurs once the fuse reaches the endpoint, calls activate()"""
        if not self.triggered:
            self.triggered = True
            self.activate()

    def reset(self):
        """Resets the endpoint to be activatable again"""
        self.triggered = False
