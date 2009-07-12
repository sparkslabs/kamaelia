#!/usr/bin/python

import sys
import os
import re
import Axon

from Kamaelia.Chassis.Graphline import Graphline 
from Kamaelia.Chassis.Pipeline import Pipeline

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
                        print "missing argument: --"+key, "-"+k
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
    print 
    print "Usage:"
    print "\t", sys.argv[0], "[options] [flags]",
    
    #
    # Display how the rest of the line is used - eg "files", if at all
    #
    # Some programs may use the unnamed options on the command line
    if usesrest:
      print usesrest
    else:
      print
    
    #
    # Display options, then flags. Required options first.
    #
    print
    print "Flags/options marked '**' below are required."
    print 
    print "Options:"
    for l,r,d in lines:
        print l + (w-len(l))*" " + "  " + r
        if d and d != '':
            print w*" "+ "  Default:",d
            print

    print "Flags:"
    for l,r in flaglines:
        print l + (w-len(l))*" " + "  " + r

class Find(Axon.Component.component):
    path = "."
    walktype = "a"
    act_like_find = True
    def find(self, path = ".", walktype="a"):
        if walktype == "a":
            addfiles = True
            adddirs = True
        elif walktype == "f":
            addfiles = True
            adddirs = False
        elif walktype == "d":
            adddirs = True
            addfiles = False

        deque = []
        deque.insert(0,  (os.path.join(path,x) for x in os.listdir(path)) )
        while len(deque)>0:
            try:
                fullentry = deque[0].next()
                if os.path.isdir(fullentry):
                    if adddirs:
                        yield fullentry
                    try:
                        X= [ os.path.join(fullentry,x) for x in os.listdir(fullentry) ]
                        deque.insert(0, iter(X))
                    except OSError:
                        if not self.act_like_find:
                            raise
                elif os.path.isfile(fullentry):
                    if addfiles:
                        yield fullentry
            except StopIteration:

                deque.pop(0)

    def main(self):
        gotShutdown = False
        for e in self.find(path = self.path, walktype=self.walktype):
            self.send(e, "outbox")
            yield 1
            if self.dataReady("control"):
                gotShutdown = True
                break

        if not gotShutdown:
            self.send(Axon.Ipc.producerFinished(), "signal")
        else:
            self.send(self.recv("control"), "signal")

class Sort(Axon.Component.component):
    def main(self):
        dataset = []
        while 1:
            for i in self.Inbox("inbox"):
                dataset.append(i)
            if self.dataReady("control"):
                break
            self.pause()
            yield 1
        dataset.sort()
        for i in dataset:
            self.send(i, "outbox")
            yield 1
        self.send(self.recv("control"), "signal")

class Grep(Axon.Component.component):
    pattern = "."
    invert = False
    def main(self):
        match = re.compile(self.pattern)
        while 1:
            for i in self.Inbox("inbox"):
                if match.search(i):
                    if not self.invert:
                        self.send(i, "outbox")
                else:
                    if self.invert:
                        self.send(i, "outbox")
            if self.dataReady("control"):
                break
            self.pause()
            yield 1
        self.send(self.recv("control"), "signal")

class TwoWayBalancer(Axon.Component.component):
    Outboxes=["outbox1", "outbox2", "signal1","signal2"]
    def main(self):
        c = 0
        while 1:
            yield 1
            for job in self.Inbox("inbox"):
                if c == 0:
                    dest = "outbox1"
                else:
                    dest = "outbox2"
                c = (c + 1) % 2

                self.send(job, dest)
                job = None
            if not self.anyReady():
                self.pause()
            if self.dataReady("control"):
                break
        R=self.recv("control")
        self.send(R, "signal1")
        self.send(R, "signal2")


class Transcoder(Axon.ThreadedComponent.threadedcomponent):
    # command = 'ffmpeg >transcode.log 2>&1 -i "%(SOURCEFILE)s" -s 640x360 -vcodec mpeg4 -acodec copy -vb 1500000 %(ENCODINGNAME)s'
    command = 'mencoder >transcode.log 2>/dev/null "%(SOURCEFILE)s" -ovc lavc -oac mp3lame -ffourcc mp4 -lavcopts acodec=copy:vbitrate=1500 -vf scale=640:-2 -o %(ENCODINGNAME)s'
    def main(self):
        while 1:
            for sourcefile in self.Inbox("inbox"):
                shortname = os.path.basename(sourcefile)
                encoding_name = shortname.replace(".mp4", ".avi")
                finalname = sourcefile.replace(".mp4", ".avi")
                # Do the actual transcode
                print "TRANSCODING", sourcefile, encoding_name
                os.system( self.command % {"SOURCEFILE": sourcefile, "ENCODINGNAME":encoding_name})

                # file is transcoded, move to done
                print "MOVING DONE FILE", sourcefile, os.path.join("done", sourcefile)
                os.rename(sourcefile, os.path.join("done", sourcefile))

                # Move encoded version to upload queue
                upload_name = os.path.join( "to_upload", encoding_name)
                print "MOVING TO UPLOAD QUEUE", encoding_name, upload_name
                os.rename(encoding_name, upload_name )

                # And tell the encoder to upload it please
                print "SETTING OFF UPLOAD",upload_name, finalname
                self.send( (upload_name, finalname), "outbox")
                print "-----------------"
            if self.dataReady("control"):
                break
        self.send(self.recv("control"), "signal")

class Uploader(Axon.ThreadedComponent.threadedcomponent):
    command = "ftpput --server=%(HOSTNAME)s --verbose --user=%(USERNAME)s --pass=%(PASSWORD)s --binary --passive %(UPLOADFILE)s"
    username = ""
    password = ""
    hostname = "ftp.blip.tv"
    def main(self):
        if self.username != "" and self.password != "":
            while 1:
                for (upload_name, finalname) in self.Inbox("inbox"):
                    print "UPLOADING", upload_name
                    os.system( self.command % {
                                            "HOSTNAME":self.hostname,
                                            "USERNAME":self.username,
                                            "PASSWORD":self.password,
                                            "UPLOADFILE":upload_name,
                                         } )
                    print "MOVING", upload_name, "TO", os.path.join("encoded", finalname)
                    os.rename(upload_name, os.path.join("encoded", finalname))
                    print "-----------------"

                if self.dataReady("control"):
                    break
                if not self.anyReady():
                    self.pause()

        if self.dataReady("control"):
            self.send(self.recv("control"), "signal")
        else:
            self.send(Axon.Ipc.shutdownMicroprocess(), "signal")

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
