#!/usr/bin/env python

from AIMHarness import AIMHarness
from IRC.Text import TextDisplayer, Textbox
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Util.PureTransformer import PureTransformer

def sendTo(recipient, text):
    return ("message", recipient, text)

def GUIthing(screenname, password, buddyname):
    Pipeline(Textbox(position=(0, 400)),
             PureTransformer(lambda text: sendTo(buddyname, text)),
             AIMHarness(screenname, password),
             TextDisplayer()
             ).run()

if __name__ == '__main__':
    import sys

    def parseArgs(args):
        if "-b" in args:
            buddy = args[args.index("-b") + 1]
        else:
            buddy = "Spleak"
        if "-s" in args:
            screenname = args[args.index("-s") + 1]
            password = args[args.index("-s") + 2]
        else:
            screenname, password = "kamaelia1", "abc123"
        return screenname, password, buddy

    args = parseArgs(sys.argv[1:])
    print sys.argv
    GUIthing(*args).run()
