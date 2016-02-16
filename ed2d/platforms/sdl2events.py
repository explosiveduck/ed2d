import ctypes as ct

import sdl2 as sdl

from ed2d.platforms import sdl2keymap as keymap
from ed2d.events import Events

MOUSE_LEFT = 1
MOUSE_MIDDLE = 2
MOUSE_RIGHT = 3
MOUSE_EX1 = 4
MOUSE_EX2 = 5

class SystemEvents(object):
    ''' Handles Event stuff... '''
    def __init__(self):
        sdl.SDL_InitSubSystem(sdl.SDL_INIT_EVENTS)

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
            elif event.type == sdl.SDL_MOUSEBUTTONUP:
                eventName = 'mouse_button_up'
                data = (event.button.button, event.button.clicks, event.button.x, event.button.y)
            elif event.type == sdl.SDL_MOUSEBUTTONDOWN:
                eventName = 'mouse_button_down'
                data = (event.button.button, event.button.clicks, event.button.x, event.button.y)
            else:
                # Will add more event types later
                pass

            if eventName is not None:
                Events.broadcast_event(eventName, data)

__all__ = ['Events']
