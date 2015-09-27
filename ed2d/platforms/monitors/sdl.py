
import sdl2 as sdl


class DisplayMode(object):
    def __init__(self):
        self.width = None
        self.height = None
        self.format = None
        self.refresh_rate = None


class Monitor(object):
    def __init__(self):
        self.supportedModes = None
        self.displayMode = None
        self.primary = None

        # Current rect info
        self.right = None
        self.left = None
        self.bottom = None
        self.top = None

        self.id = None


def _sdl2_mode_convert(sdlMode):
    mode = DisplayMode()

    # mode.format = sdlMode.format
    mode.width = sdlMode.w
    mode.height = sdlMode.h
    mode.refresh_rate = sdlMode.refresh_rate

    return mode


def _sdl2_mode_init():
    dispMode = sdl.SDL_DisplayMode()

    dispMode.format = sdl.SDL_PIXELFORMAT_UNKNOWN
    dispMode.w = 0
    dispMode.h = 0
    dispMode.refresh_rate = 0

    return dispMode


def _cmp_displ_modes(mode1, mode2):
    return (mode1.width == mode2.width and
            mode1.height == mode2.heigt and
            mode1.refresh_rate == mode2.refresh_rate and
            mode1.format == mode2.format)


class Monitors(object):
    def __init__(self):
        self.monitors = None
        self.monitorCount = None
        self.displayModes = []
        self.update_monitors()
        self.update_display_modes()

    def _find_matching_mode(self, mode):
        modeMatch = None
        for dispMode in self.displayModes:
            if _cmp_displ_modes(dispMode, mode):
                modeMatch = dispMode
                break
        return modeMatch

    def update_display_modes(self):
        '''Re-aquire display mode data from sdl2'''
        for dis in self.monitors:
            modeCount = sdl.SDL_GetNumDisplayModes(dis.id)
            dis.supportedModes = []

            for modeID in range(modeCount):

                dispMode = _sdl2_mode_init()

                sdl.SDL_GetDisplayMode(dis.id, modeID, dispMode)

                mode = _sdl2_mode_convert(dispMode)

                for disMode in self.displayModes:
                    if _cmp_displ_modes(disMode, mode):
                        dis.supportedModes.append(disMode)
                        continue
                    else:
                        dis.supportedModes.append(mode)
                        self.displayModes.append(mode)

                if not self.displayModes:
                    dis.supportedModes.append(mode)
                    self.displayModes.append(mode)

                currDisplay = _sdl2_mode_init()

                sdl.SDL_GetCurrentDisplayMode(dis.id, currDisplay)

                currMode = _sdl2_mode_convert(currDisplay)
                dis.displayMode = self._find_matching_mode(currMode)

    def update_monitors(self):
        '''Re-aquire monitor data from sdl2'''

        self.monitorCount = sdl.SDL_GetNumVideoDisplays()

        monitors = []

        for i in range(self.monitorCount):

            rect = sdl.SDL_Rect()
            sdl.SDL_GetDisplayBounds(i, rect)

            monitor = Monitor()
            monitor.id = i

            monitor.left = rect.x
            monitor.right = rect.x + rect.w
            monitor.top = rect.y
            monitor.bottom = rect.y + rect.h

            if monitor.left == 0 and monitor.top == 0:
                monitor.primary = True
            else:
                monitor.primary = False

            monitors.append(monitor)

        self.monitors = monitors

    def get_monitor_at(self, xPos, yPos):
        """ Returns a monitor based on a single point """
        monitorFound = None
        for monitor in self.monitors:
            if xPos <= monitor.right and xPos >= monitor.left:
                if yPos <= monitor.bottom and yPos >= monitor.top:
                    monitorFound = monitor

        return monitorFound

    def get_primary_monitor(self):
        '''Get the monitor located at 0 0. This is the primary.'''
        for monitor in self.monitors:
            if monitor.left == 0 and monitor.top == 0:
                return monitor

    # Currently not possible with sdl2 with the public api.
    # def set_monitor_defaults(self, monitor):
    #     '''Switch monitor back to default display mode'''
    #     mode = sdl.SDL_DisplayMode()
    #     sdl.SDL_GetDesktopDisplayMode(monitor.id, mode)
