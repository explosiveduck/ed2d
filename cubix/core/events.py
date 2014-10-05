import ctypes as ct

import sdl2 as sdl

class Events(object):
    ''' Handles Event stuff... '''
    def __init__(self):
        sdl.SDL_InitSubSystem(sdl.SDL_INIT_EVENTS)

        self.listeners = []

    def add_listener(self, listener):
        '''
        Add an event processing listener.
        An event listener is just a function that accepts 2 arguments.
        '''
        self.listeners.append(listener)

    def remove_listener(self, listener):
        ''' Remove specified event listener '''
        if not listener in self.listeners:
            self.listener.remove()

    def broadcast_event(self, event, args):
        ''' Send out an event to all event listeners '''
        for listener in self.listeners:
            listener(event, args)

    def process(self):
        '''
        Processes the events polled from sdl.
        Custom events might be a possiblility if we need them.
        '''
        
        event = sdl.SDL_Event()

        while sdl.SDL_PollEvent(ct.byref(event)):

            eventName = None
            data = None

            if event.type == sdl.SDL_QUIT:
                eventName = 'quit'
                data = ()
            if event.type == sdl.SDL_WINDOWEVENT:
                winEvent = event.window.event
                # For now this will only support one window
                # If we want two later on then we can do it then.
                if winEvent == sdl.SDL_WINDOWEVENT_CLOSE:
                    eventName = 'window_close'
                    data = ()
            else:
                # Will add more event types later
                pass

            if not eventName is None:
                self.broadcast_event(eventName, data)