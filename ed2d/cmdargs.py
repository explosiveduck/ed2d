import argparse

class _CmdArgs(object):
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.letterArgs = []
        self.args = None

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
                print ('All possible short arguments are taken for this name.')
                return

            args.append('-' + letter)

        self.parser.add_argument(*args, type=argType, help=argHelp)

        self.parse_args()

        return self.args[name]

    def parse_args(self):
        self.args = vars(self.parser.parse_args())

CmdArgs = _CmdArgs()
