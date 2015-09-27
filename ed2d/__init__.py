def _init():
    # any modules that need to be initialized early will be imported here
    import ed2d.debug
    ed2d.debug._debug('Debug module init.')

_init()
