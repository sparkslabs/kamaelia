#!/usr/bin/python

import os
import Axon

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
