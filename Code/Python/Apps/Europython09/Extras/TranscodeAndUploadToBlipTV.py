#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2010 British Broadcasting Corporation and Kamaelia Contributors(1)
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://www.kamaelia.org/AUTHORS - please extend this file,
#     not this notice.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import sys
import os
import re
import Axon

from Kamaelia.Chassis.Graphline import Graphline 
from Kamaelia.Chassis.Pipeline import Pipeline

from Kamaelia.Apps.Europython09.Options import parseargs, showHelp, readJSONConfig, checkArgs, needToShowUsage, showUsageBasedOnHowUsed

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
    
conf_args = readJSONConfig("transcode.conf")
conf_args.update (readJSONConfig(os.path.expanduser("~/.kamaelia/transcode.conf")))

args = parseargs( sys.argv[1:], *argspec) 
args.update(conf_args)    # FIXME: unify args & conf_args in a nicer, more sensible way.

if needToShowUsage(args, argspec):
    showUsageBasedOnHowUsed(args, argspec)
    print "\nNote: This program can also read a JSON formatted config file called transcode.conf"
    print "for these config options"
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
