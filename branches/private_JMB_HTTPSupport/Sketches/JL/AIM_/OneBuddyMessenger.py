#!/usr/bin/env python

#the locations of AIMHarness and IRC.Text may change.

from AIMHarness import AIMHarness
from IRC.Text import TextDisplayer, Textbox
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.Util.PureTransformer import PureTransformer

def sendTo(recipient, text):
    return ("message", recipient, text)

def outformat(data, buddyname):
    if data[0] == "buddy online" and data[1]["name"] ==  buddyname:
        return "%s is online" % buddyname
    elif data[0] == "message" and data[1] == buddyname:
        return "%s: %s" % (buddyname, data[2])
    elif data[0] == "error":
        ": ".join(data)

def SimpleAIMClient(screenname, password, buddyname):
    Pipeline(Textbox(position=(0, 400)),
             PureTransformer(lambda text: sendTo(buddyname, text)),
             AIMHarness(screenname, password),
             PureTransformer(lambda tup: outformat(tup, buddyname)),
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
    SimpleAIMClient(*args).run()
