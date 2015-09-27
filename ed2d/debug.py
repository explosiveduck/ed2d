from ed2d.cmdargs import CmdArgs

debug = CmdArgs.add_arg('debug', bool, 'Enable debug output.')

def _debug(*args):
    if debug:
        print(*args)
