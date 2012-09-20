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
                    print ("UPLOADING", upload_name)
                    os.system( self.command % {
                                            "HOSTNAME":self.hostname,
                                            "USERNAME":self.username,
                                            "PASSWORD":self.password,
                                            "UPLOADFILE":upload_name,
                                         } )
                    print ("MOVING", upload_name, "TO", os.path.join("encoded", finalname))
                    os.rename(upload_name, os.path.join("encoded", finalname))
                    print ("-----------------")

                if self.dataReady("control"):
                    break
                if not self.anyReady():
                    self.pause()

        if self.dataReady("control"):
            self.send(self.recv("control"), "signal")
        else:
            print ("Needed username & password to do upload!")
            self.send(Axon.Ipc.shutdownMicroprocess(), "signal")
