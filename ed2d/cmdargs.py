import argparse

class ArgParseWrapper(argparse.ArgumentParser):
    '''Overide the default parse_args to not error out with unused args.'''
    def parse_args(self, args=None, namespace=None):
        args, argv = self.parse_known_args(args, namespace)
        return args

class _CmdArgs(object):
    def __init__(self):
        self.parser = ArgParseWrapper(add_help=False)
        self.letterArgs = []
        self.args = None
        self.argsParsed = False

    def set_description(self, desc):
        self.parser.description = desc

    def add_arg(self, name, argType, argHelp, noShort=False):

        args = []

        args.append('--' + name)

        if not noShort:
            # Check through 
            letter = None
            for i in range(len(name)):
                if name[i] in self.letterArgs:
                    continue
                self.letterArgs.append(name[i])

                letter = name[i]
                break
            else:
                print('All possible short arguments are taken for this name.')
                return

            args.append('-' + letter)

        self.parser.add_argument(*args, type=argType, help=argHelp)

        return vars(self.parser.parse_args())[name]

    def parse_args(self):
        # Add the help option/action after all arguments
        self.parser.add_argument('-h', '--help',
            action='help',
            default=argparse.SUPPRESS, help='show this help message and exit')
        self.args = vars(self.parser.parse_args())
        self.argsParsed = True

CmdArgs = _CmdArgs()

__all__ = [CmdArgs, ]
