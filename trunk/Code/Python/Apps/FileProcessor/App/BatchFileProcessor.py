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
import time
import Axon
import Image
from Kamaelia.Chassis.Pipeline import Pipeline
from Kamaelia.File.UnixProcess import UnixProcess

class DirectoryWatcher(Axon.ThreadedComponent.threadedcomponent):
    watch = "uploads"
    def main(self):
        S = None
        while True:
            N = os.stat(self.watch)
            if S != N:
                if S != None:
                    if S.st_mtime != N.st_mtime:
                        print "uploads changed, processing", S==N, list(S), list(N)
                        S = N
                        self.send(self.watch, "outbox")
                else:
                    print "initialising, checking uploads", S==N, S, list(N)
                    S = N
                    self.send(self.watch, "outbox")
            time.sleep(1)

class FileProcessor(Axon.Component.component):
    Inboxes = {
        "inbox": "-",
        "control": "-",
        "_unixprocessdone": "-",
    }
    def Inline(self, X, outbox="outbox", signal="signal", inbox="inbox", control="control"):
        def Y(X, outbox,signal,inbox,control):
            L1 = self.link((X, signal), (self, control))
            L2 = self.link((X, outbox), (self, inbox))
            X.activate()
            yield 1
            while not self.dataReady(control):
                yield 1
            self.recv(control)
            self.unlink(L1)
            self.unlink(L2)
            del X

        return Axon.Ipc.WaitComplete(Y(X,outbox,signal,inbox,control))

    def system(self, command):
        return self.Inline( UnixProcess(command+";sleep 0.2"), control="_unixprocessdone" )

    def processfile(self, directory, filename):
        print " ... processing:", filename
        yield 1
    def processfiles(self, directory):
        print "Directory changed: ", directory
        for filename in os.listdir(directory):
            for i in self.processfile(directory, filename):
               yield i

    def main(self):
        while True:
            while not self.anyReady():
                self.pause()
                yield 1
            for message in self.Inbox("inbox"):
                for i in self.processfiles(message):
                    yield i
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
                dest_file1 = self.destdir + "/" + thefile + "/" + "nanothumb" + ".jpg"
                dest_file2 = self.destdir + "/" + thefile + "/" + size + ".jpg"


                print "convert %s -crop %dx%d+0+0 -resize 18x %s" % (sourcefile, side_size,side_size, dest_file1)
                yield self.system( "convert %s -crop %dx%d+0+0 -resize 18x %s" % (sourcefile, side_size,side_size, dest_file1) )

                print "convert %s -crop %dx%d+0+0 -resize 40x %s" % (sourcefile, side_size,side_size, dest_file2)
                yield self.system( "convert %s -crop %dx%d+0+0 -resize 40x %s" % (sourcefile, side_size,side_size, dest_file2) )

            else:
                width = self.sizes[size]
                dest_filename = size + "-" + filename
                full_dest_filename = os.path.join(self.destdir, dest_filename)

                full_dest_filename = self.destdir + "/" + thefile + "/" + size + ".jpg"

                resize_arg = "-resize %dx" % width

                print "convert", sourcefile, resize_arg, full_dest_filename
                yield self.system( " ".join( [ "convert", sourcefile, resize_arg, full_dest_filename ]) )

        os.unlink(sourcefile)


class ImageMover(FileProcessor):
    destdir = "/tmp"
    def processfile(self, directory, filename):
        extn = filename[filename.rfind("."):].lower()
        if extn in [ ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".ppm", ".pnm"]:
            os.rename( os.path.join(directory, filename),
                       os.path.join(self.destdir, filename)
                     )
        yield 1

class VideoTranscoder(FileProcessor):
    destdir = "moderate"
    conversion = "ffmpeg -i %(sourcefile)s %(deststem)s.flv"
    template = "player-template.html"
    def processfile(self, directory, filename):
        thefile = filename[:filename.rfind(".")]

        sourcefile = os.path.join(directory, filename)
        command = self.conversion % {
                                     "sourcefile" : sourcefile,
                                     "deststem"   : self.destdir + "/" + thefile,
                                    }
        yield self.system( command )

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
        yield 1

def read_config(filename):

    conf = {}
    try:
        F = open(filename)
        for line in F:
            line = line.strip().rstrip()
            if line == "":
               continue
            if line[0] == "#":
               continue
            try:
                key, value = line.split()
                conf[key] = value
            except:
                print "BAD CONFIG LINE: ", repr(line)

        F.close()
    except:
        print "General error parsing", filename
    return conf

conf = {}

default_conf = {
    "main_incoming_queue"    : "/tmp/uploads",
    "image_queue"            : "/tmp/uploads/images",
    "video_queue"            : "/tmp/uploads/videos",
    "image_moderation_queue" : "/tmp/moderate/images",
    "video_moderation_queue" : "/tmp/moderate/videos",
}

local_def_conf = read_config("/etc/batch_converter.conf.dist")
local_conf = read_config("/etc/batch_converter.conf")

conf.update(default_conf)
conf.update(local_def_conf)
conf.update(local_conf)

Pipeline(
    DirectoryWatcher(watch = conf["main_incoming_queue"]),
    ImageMover(destdir = conf["image_queue"]),
).activate()

Pipeline(
    DirectoryWatcher(watch = conf["image_queue"]),
    ImageTranscoder(destdir = conf["image_moderation_queue"]),
).activate()

Pipeline(
    DirectoryWatcher(watch = conf["main_incoming_queue"]),
    VideoMover(destdir = conf["video_queue"]),
).activate()

Pipeline(
    DirectoryWatcher(watch = conf["video_queue"]),
    VideoTranscoder(destdir = conf["video_moderation_queue"]),
).run()
