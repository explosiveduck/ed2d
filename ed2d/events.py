
# TODO - Add support for event filters so we dont have to rebroadcast everything
# to listeners that wont use most of it.

class EventQueue(object):
    def __init__(self):
        self.listeners = []

    def add_listener(self, listener):
        '''
        Add an event processing listener.
        An event listener is just a function that accepts 2 arguments.
        '''
        self.listeners.append(listener)

    def remove_listener(self, listener):
        ''' Remove specified event listener '''
        if listener not in self.listeners:
            self.listener.remove()

    def broadcast_event(self, event, args):
        ''' Send out an event to all event listeners '''
        for listener in self.listeners:
            listener(event, args)

Events = EventQueue()
