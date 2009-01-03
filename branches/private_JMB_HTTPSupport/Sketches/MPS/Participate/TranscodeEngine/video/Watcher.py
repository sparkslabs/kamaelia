#!/usr/bin/python

import os
import time
import Axon
import Image
from Kamaelia.Chassis.Pipeline import Pipeline

class DirectoryWatcher(Axon.ThreadedComponent.threadedcomponent):
    watch = "upload"
    sleeptime = 10
    def main(self):
        S = None
        while True:
            N = os.stat(self.watch)
            if S != N:
                if S != None:
                    if S.st_mtime != N.st_mtime:
                        print "uploads changed, processing", S==N, list(S), list(N)
                        S = N
                        time.sleep(2)
                        self.send(self.watch, "outbox")
                else:
                    print "initialising, checking uploads", S==N, S, list(N)
                    S = N
                    self.send(self.watch, "outbox")
            time.sleep(self.sleeptime)

class FileProcessor(Axon.Component.component):
    def processfile(self, directory, filename):
        print " ... processing:", filename
    def processfiles(self, directory):
        print "Directory changed: ", directory
        for filename in os.listdir(directory):
            self.processfile(directory, filename)

    def main(self):
        while True:
            while not self.anyReady():
                self.pause()
                yield 1
            for message in self.Inbox("inbox"):
                self.processfiles(message)
            yield 1

class ImageTranscoder(FileProcessor):
    destdir = "moderate"
    sizes = {
        "large" : 626,
        "normal" : 466,
        "medium" : 306,
        "thumb" : 146,
        "minithumb" : 66,
        "microthumb" : 18,
    }
    def processfile(self, directory, filename):
        thefile = filename[:filename.rfind(".")]
        file_ending = filename[filename.rfind("."):]
        print thefile
        try:
            os.makedirs( os.path.join( self.destdir , thefile ) )
        except OSError:
            return
        
        sourcefile = os.path.join(directory, filename)
        
        try:
            X = Image.open(sourcefile)
            size = X.size
            X = None
            side_size = min(*size)
        except IOError:
            return
        for size in self.sizes:
            if size == "microthumb":
                dest_file1 = self.destdir + "/" + thefile + "/" + "nanothumb" + file_ending
                dest_file2 = self.destdir + "/" + thefile + "/" + size + file_ending
                                
                
                print "convert %s -crop %dx%d+0+0 -resize 18x %s" % (sourcefile, side_size,side_size, dest_file1)
                os.system( "convert %s -crop %dx%d+0+0 -resize 18x %s" % (sourcefile, side_size,side_size, dest_file1) )

                print "convert %s -crop %dx%d+0+0 -resize 40x %s" % (sourcefile, side_size,side_size, dest_file2)
                os.system( "convert %s -crop %dx%d+0+0 -resize 40x %s" % (sourcefile, side_size,side_size, dest_file2) )
                
            else:            
                width = self.sizes[size]
                dest_filename = size + "-" + filename
                full_dest_filename = os.path.join(self.destdir, dest_filename)
                
                full_dest_filename = self.destdir + "/" + thefile + "/" + size + file_ending
                
                resize_arg = "-resize %dx" % width
                
                print "convert", sourcefile, resize_arg, full_dest_filename
                os.system( " ".join( [ "convert", sourcefile, resize_arg, full_dest_filename ]) )

        os.unlink(sourcefile)

class VideoTranscoder(FileProcessor):
    destdir = "moderate"
    conversion = "/usr/local/bin/ffmpeg -i %(sourcefile)s -ar 11025 %(deststem)s.flv"
    template = "player-template.html"
    def processfile(self, directory, filename):
        thefile = filename[:filename.rfind(".")]
                
        sourcefile = os.path.join(directory, filename)
        command = self.conversion % {
                                     "sourcefile" : sourcefile,
                                     "deststem"   : self.destdir + "/" + thefile,
                                    }
        os.system( command )
        
        F = open(self.template)
        t = F.read()
        F.close()
        
        X = t % {"videofile" : thefile + ".flv" }
        F = open(self.destdir + "/" + thefile + ".html", "w")
        F.write(X)
        F.close()

        os.unlink(sourcefile)

class VideoMover(FileProcessor):
    destdir = "/tmp"
    extensions = [ ".3gp", ".3gp2", ".3gpp", ".asf", ".asx", ".avi", ".dv",
                   ".flv", ".m1v", ".m4e", ".m4u", ".m4v", ".mjp", ".moov",
                   ".mov", ".movie", ".mp4", ".mpe", ".mpeg", ".mpg", ".qt",
                   ".rm", ".swf", ".ts", ".wmv"]
    def processfile(self, directory, filename):
        extn = filename[filename.rfind("."):].lower()
        if extn.lower() in self.extensions:
            os.rename( os.path.join(directory, filename),
                       os.path.join(self.destdir, filename)
                     )
Pipeline(
    DirectoryWatcher(watch = "/srv/www/sites/bicker.kamaelia.org/cgi/app/uploads"),
    VideoMover(destdir = "/srv/www/sites/bicker.kamaelia.org/uploads/videos"),
).activate()


Pipeline(
    DirectoryWatcher(watch = "/srv/www/sites/bicker.kamaelia.org/uploads/videos"),
    VideoTranscoder(destdir = "/srv/www/sites/bicker.kamaelia.org/moderate/videos"),
).run()


