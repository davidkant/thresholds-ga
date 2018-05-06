import OSC
import time
from threading import Thread

class PyServer: 
    """A very basic server."""

    def __init__(self, address, timeout):
        self._running = False
        self.address = address
        self.timeout = timeout
    
    def handle(self):
        """Handle requests."""
        while self._running:
            self.server.handle_request()

    def start(self):
        """Start the server."""
        self.server = OSC.OSCServer(self.address)
        self.server.timeout = self.timeout
        self._running = True
        self.t = Thread(target=self.handle, args=())
        self.t.start()
        return self
        
    def stop(self):
        """Stop the server."""
        self._running = False
        time.sleep(1) # wait to finish final cycle
        self.server.close()
        return self

    def is_running(self):
        """Is it running?"""
        return self._running

    def __repr__(self):
        return '<PyServer(address: {0.address!r}, timeout: {0.timeout!r})>'.format(self)

if __name__ == "__main__":
    s = PyServer(('127.0.0.1', 57126), 666).start()
