#!/usr/bin/python

import os
import Axon

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
            print "Needed username & password to do upload!"
            self.send(Axon.Ipc.shutdownMicroprocess(), "signal")
