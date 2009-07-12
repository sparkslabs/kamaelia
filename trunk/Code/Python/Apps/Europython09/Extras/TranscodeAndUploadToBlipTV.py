#!/usr/bin/python

import sys
import os
import re
import Axon

from Kamaelia.Chassis.Graphline import Graphline 
from Kamaelia.Chassis.Pipeline import Pipeline

from Kamaelia.Apps.Europython09.Options import parseargs, showHelp
from Kamaelia.Apps.Europython09.Util import Find, Sort, Grep, TwoWayBalancer
from Kamaelia.Apps.Europython09.VideoFileTranscode import Transcoder
from Kamaelia.Apps.Europython09.FTP import Uploader

argspec = [
            { ("p", "path" ):           (".", "Directory to rummage around below for files to transcode & upload."),
              ("e", "exclude-pattern"): ("(done|encoded|unsorted|transcode.log|to_upload)", "Pattern/filespecs to exclude from walk"),
              ("u", "username"):        ("", "Username for ftp server"),
              ("p", "password"):        ("", "Password for ftp server"),
              ("s", "server"):          ("ftp.blip.tv", "FTP Server to upload to"),
            },
            [("h","help", "Show some help on how to use this")],
            ["username", "password"],
            ""
          ]

#
# Handle a reading a json encoded config file. Probably something nicer that
# this would be good, but this will do for now.
#
if os.path.exists("transcode.conf"):
    import cjson
    g = open("transcode.conf", "rb")
    Y_ = g.read()
    g.close()
    conf_args = cjson.decode(Y_)
else:
    conf_args = {}

args = parseargs( sys.argv[1:], *argspec) 

# FIXME: unify args & conf_args in a nicer, more sensible way.
args.update(conf_args)

#
# This can probably be automated base on "required" part of argspec.
#  Not yet done though!
#
if args["help"] or args["username"]=="" or args["password"]=="":
    if not args["help"]:
        print "USAGE ERROR:"
        if args["username"] == "":
            print "\tusername must be given"

        if args["password"] == "":
            print "\tpassword must be given"
        print 

    showHelp(argspec)
    sys.exit(0)

Graphline(
    FILES = Pipeline(
                Find(path=args["path"],walktype="f"),
                Sort(),
                Grep(pattern=args["exclude-pattern"], invert = True),
            ),
    SPLIT = TwoWayBalancer(), # Would probably be nicer as a chassis, or a customised PAR chassis
    CONSUME1 = Pipeline( 
                    Transcoder(),
                    Uploader(username=args["username"],  # Would be better to pass to a single uploader really
                             password=args["password"],
                             hostname=args["server"]),
               ),
    CONSUME2 = Pipeline( 
                    Transcoder(),
                    Uploader(username=args["username"],  # Would be better to pass to a single uploader really
                             password=args["password"],
                             hostname=args["server"]),
               ),
    linkages = {
        ("FILES","outbox"):("SPLIT","inbox"),
        ("SPLIT","outbox1"):("CONSUME1","inbox"),
        ("SPLIT","outbox2"):("CONSUME2","inbox"),

        ("FILES","signal"):("SPLIT","control"),
        ("SPLIT","signal1"):("CONSUME1","control"),
        ("SPLIT","signal2"):("CONSUME2","control"),
    }
).run()
