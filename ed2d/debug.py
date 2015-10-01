from __future__ import print_function
from ed2d.cmdargs import CmdArgs

debugEnabled = CmdArgs.add_arg('debug', bool, 'Enable debug output.')

def debug(*args):
    if debugEnabled:
        print(*args)
