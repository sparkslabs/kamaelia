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

# Components for using Spee Encoding

import speex
from Axon import Component

class SpeexEncode(Component.component):

    def __init__(self, quality=8):

        super(SpeexEncode, self).__init__()
        self.quality = quality
    
    def main(self):

        speexobj = speex.new(self.quality)

        while 1:

            if self.dataReady("inbox"):

                data = self.recv("inbox")
                #print data
                ret = speexobj.encode(data)

                if ret is not "":           # Speex objects use internal buffering
                    #print ret
                    self.send(ret, "outbox")

            yield 1

class SpeexDecode(Component.component):


    def __init__(self, quality=8):

        super(SpeexDecode, self).__init__()
        self.quality = quality
            
    def main(self):

        speexobj = speex.new(self.quality)

        while 1:

            if self.dataReady("inbox"):

                ret = speexobj.decode(self.recv("inbox"))


                if ret is not "":     # Speex objects use internal buffering

                    result = []
                    for mixed in ret:
                        if mixed < 0:
                            mixed = 65536 + mixed
                        mixed_lsb= mixed %256
                        mixed_msb= mixed >>8
                        result.append(chr(mixed_lsb))
                        result.append(chr(mixed_msb))

                    data = "".join(result)
                    #print ret
                    #ret = str(ret)
                    self.send(data, "outbox")

            yield 1
