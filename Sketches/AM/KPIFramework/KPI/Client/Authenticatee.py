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

import struct
import Axon
from KPI.Crypto import xtea


class Authenticatee(Axon.Component.component):
    Inboxes = {"inbox" : "authentication and data packets"}
    Outboxes = {"outbox" : "authentication",
                "encout" : "encrypted data packets",
                "notifykey" : "notify key"}

    def __init__(self, kpiuser):
      super(Authenticatee,self).__init__()
      self.kpiuser = kpiuser
   
    
    def main(self):
        userid = self.kpiuser.getID()
        data = xtea.xtea_encrypt(self.kpiuser.getRootKey(),
                                 struct.pack('!2L',0, userid))
        print "encrypting user id with user key", self.kpiuser.getID(), self.kpiuser.getRootKey()
        self.send(data, "outbox")
        yield 1

        while not self.dataReady("inbox"):
            yield 1
        data = self.recv("inbox")
        temp = xtea.xtea_decrypt(self.kpiuser.getUserKey(), data)
        padding, challenge = struct.unpack('!2L',temp)
        response = challenge+1
        print "received challenge",challenge
        print "sending response", response
        data = xtea.xtea_encrypt(self.kpiuser.getUserKey(),
                                 struct.pack('!2L',0, response))
        
        
        self.send(data, "outbox")
        yield 1
        while not self.dataReady("inbox"):
            yield 1
        data = self.recv("inbox")
        if data == "SUCCESS":
            print "authentication success"
        else:
            print "authenication failure"
            return

        #decode data
        while 1:
            while self.dataReady("inbox"):
                data = self.recv("inbox")
                print "decoder", data
                if data.startswith("KEY"):
                    index = len("KEY")
                    #get the ID
                    padding,ID = struct.unpack("!2L", data[index:index+8])
                    print "****ID****", ID
                    key = ""
                    try:
                        key = self.kpiuser.getKey(ID)
                    except KeyError:
                        pass #the key is not for me

                    if key != "":
                        enckey = data[index+8:len(data)]
                        part1 = xtea.xtea_decrypt(key, enckey[:8])
                        part2 = xtea.xtea_decrypt(key, enckey[8:16])
                        sessionkey = part1 + part2
                        print "decoded key", sessionkey
                        self.send(sessionkey, "notifykey")
                else:
                    data = data[len("DAT"):len(data)]
                    print "decoded data", data
                    self.send(data, "encout")
            yield 1
