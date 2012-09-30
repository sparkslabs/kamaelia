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

import os
import sys

def parseargs(argv, longopts, longflags, required,usesrest):
    args = {}
    for f,flag,help in longflags:
        try:
            i = argv.index("--"+flag)
            args[flag] = True
            del argv[i]
        except ValueError:
            try:
                i = argv.index("-"+f)
                args[flag] = True
                del argv[i]
            except ValueError:
                args[flag] = False

    for k, key in longopts:
        try:
            i = argv.index("--"+key)
            F = longopts[k,key][0].__class__(argv[i+1])
            args[key] = F
            del argv[i+1]
            del argv[i]
        except ValueError:
            try:
                i = argv.index("-"+k)
                F = longopts[k,key][0].__class__(argv[i+1])
                args[key] = F
                del argv[i+1]
                del argv[i]
            except ValueError:
                if longopts[k,key][0] == None:
                    if not args.get("help", args.get("h", False)):
                        print ("missing argument: --"+key + " -"+k)
                        sys.exit(0)
                args[key] = longopts[k,key][0]


    rest = [a for a in argv if len(argv)>0 and a[0] != "-"]
    args["__anon__"] = rest
    return args

def showHelp(argspec):
    #FIXME: A little fragile, but nice
    
    #
    # First extract some information from the argspec
    # Next format options, then flags
    # Then display header
    # Then options, in 2 columns based on formatting (left/right/defaults)
    # Then flags, in 2 columns (left/right)
    # 
    longopts, longflags,required,usesrest = argspec

    # Build left, right and defaults parts of options lines
    # We do this twice
    lines = []
    rlines, olines = [],[]
    for k,key in longopts:
        l = ""
        if key in required:
            l += "  **  "
        else:
            l += "      "
        if k:
            l += "-"+k+"  "
        if key:
            l += "--"+key
        r = ""
        if longopts[k,key][1]:
            r += longopts[k,key][1]
        d = longopts[k,key][0]
        if key in required:
            rlines.append((l,r,d))
        else:
            olines.append((l,r,d))
    lines = rlines + olines

    # Build left and right halves of flag lines
    flaglines = []
    for f,flag,help in longflags:
        l = ""
        l +=  "      "
        if f:
            l +=  "-"+f+"  "
        if flag:
            l +=  "--"+flag+"  "
        r = ""
        if help:
            r = help
        flaglines.append((l,r))

    # Find out the maximum width flag/option/etc for formatting.
    w = 0 
    for l,_,_ in lines:
        w = max(len(l),w)

    for l,_ in flaglines:
        w = max(len(l),w)

    #
    # Display usage header
    #
    print ("") 
    print ("Usage:")
    print ("\t" + sys.argv[0]+ " [options] [flags]")
    
    #
    # Display how the rest of the line is used - eg "files", if at all
    #
    # Some programs may use the unnamed options on the command line
    if usesrest:
      print (usesrest)
    else:
      print ("")
    
    #
    # Display options, then flags. Required options first.
    #
    print ("")
    print ("Flags/options marked '**' below are required.")
    print ("")
    print ("Options:")
    for l,r,d in lines:
        print (l + (w-len(l))*" " + "  " + r)
        if d and d != '':
            print (w*" "+ "  Default: " + str(d))
            print ("") 

    print ("Flags:")
    for l,r in flaglines:
        print (l + (w-len(l))*" " + "  " + r)


if __name__ == "__main__":

    import os
    import pprint

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
            print ("USAGE ERROR:")
            if args["username"] == "":
                print ("\tusername must be given")

            if args["password"] == "":
                print ("\tpassword must be given")
            print ("") 

        showHelp(argspec)
        sys.exit(0)

    pprint.pprint(args)

#
# Handle a reading a json encoded config file. Probably something nicer that
# this would be good, but this will do for now.
#
def readJSONConfig(path):
    if os.path.exists(path):
        import cjson
        g = open(path, "rb")
        Y_ = g.read()
        g.close()
        conf_args = cjson.decode(Y_)
    else:
        conf_args = {}
    return conf_args

def checkArgs(args, argspec):
    argsOK = True
    missing = []
    for required in argspec[2]:
        default = None
        for k,key in argspec[0]:
            if key != required:
                continue
            default = argspec[0][k,key][0]
            break
        if args[required] == default:
           missing.append(required)
           argsOK = False
    return argsOK, missing

def needToShowUsage(args, argspec):
    argsOK, missing = checkArgs(args, argspec)
    return args["help"] or not argsOK

def showUsageBasedOnHowUsed(args, argspec):
    argsOK, missing = checkArgs(args, argspec)
    if not args["help"]:
        print ("USAGE ERROR:")
        for required in missing:
            print ("\t"+ "--"+required+ " must be given")
    showHelp(argspec)















