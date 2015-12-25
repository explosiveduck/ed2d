import ctypes as ct

import sdl2 as sdl

from ed2d.platforms import sdl2keymap as keymap

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
        if listener not in self.listeners:
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
            elif event.type == sdl.SDL_MOUSEMOTION:
                eventName = 'mouse_move'
                data = (event.motion.x, event.motion.y)
            elif event.type == sdl.SDL_WINDOWEVENT:
                winEvent = event.window
                wEventName = event.window.event
                # For now this will only support one window
                # If we want two later on then we can do it then.
                if wEventName == sdl.SDL_WINDOWEVENT_CLOSE:
                    eventName = 'window_close'
                    data = (winEvent.windowID)
                elif wEventName == sdl.SDL_WINDOWEVENT_RESIZED:
                    eventName = 'window_resized'
                    data = (winEvent.windowID, winEvent.data1, winEvent.data2)

            elif event.type == sdl.SDL_KEYUP:
                if not event.key.repeat:
                    eventName = 'key_up'
                    keyID = keymap.keymap[event.key.keysym.scancode]
                    keyName = keymap.process_key_char(event.key.keysym.sym)
                    modKeys = keymap.process_modkeys(event.key.keysym.mod)
                    data = (keyName, keyID, modKeys)

            elif event.type == sdl.SDL_KEYDOWN:
                if not event.key.repeat:
                    eventName = 'key_down'
                    keyID = keymap.keymap[event.key.keysym.scancode]
                    keyName = keymap.process_key_char(event.key.keysym.sym)
                    modKeys = keymap.process_modkeys(event.key.keysym.mod)
                    data = (keyName, keyID, modKeys)
            else:
                # Will add more event types later
                pass

            if eventName is not None:
                self.broadcast_event(eventName, data)

__all__ = ['Events']
