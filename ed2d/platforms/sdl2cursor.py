import sdl2 as sdl


def show_cursor():
    sdl.SDL_ShowCursor(sdl.SDL_ENABLE)

def hide_cursor():
    sdl.SDL_ShowCursor(sdl.SDL_DISABLE)

def get_cursor_state():
    return sdl.SDL_ShowCursor(sdl.SDL_QUERY)

def move_cursor(x, y):
    sdl.SDL_WarpMouseInWindow(None, x, y)

def set_relative_mode(enabled):
    sdl.SDL_SetRelativeMouseMode(enabled)

def is_relative():
    return bool(sdl.SDL_GetRelativeMouseMode())
