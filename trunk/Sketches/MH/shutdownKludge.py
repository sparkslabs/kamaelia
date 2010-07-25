#!/usr/bin/env python
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

class ipc(object):
    pass

class shutdown(ipc):
    pass

class shutdownMicroprocess(shutdown):

    def __new__(cls):
        if cls != shutdownNow and shutdownNow not in cls.__bases__:
            print "*** tsk tsk, creating a shutdownMicroprocess!!"
        return shutdown.__new__(shutdownNow)


class shutdownNow(shutdownMicroprocess):
    pass


class basedOnShutdownMicroprocess(shutdownMicroprocess):
    pass


# install a wrapper for isinstance() to check for shutdownMicroprocess usage
__original_isinstance = isinstance

def __isinstance(instance, types):
    if types == shutdownMicroprocess:
        print "*** tsk tsk, not in an isinstance() call!!!"
    else:
        try:
            if shutdownMicroprocess in types:
                print "*** tsk tsk, not in an isinstance() call!!!"
        except:
            pass
    return __original_isinstance(instance,types)


isinstance = __isinstance
if __name__ != "__main__":
    __builtins__["isinstance"] = __isinstance
    
else:
    print "What is a shutdownNow?"
    s=shutdownNow()
    print type(s)
    print
    print isinstance(s,shutdownNow)
    print isinstance(s,shutdownMicroprocess)
    print isinstance(s,shutdown)
    print
    
    print "What is a shutdownMicroprocess"
    s=shutdownMicroprocess()
    print type(s)
    print
    print isinstance(s,shutdownNow)
    print isinstance(s,shutdownMicroprocess)
    print isinstance(s,shutdown)
    
    print "What is a shutdownNow?"
    s=basedOnShutdownMicroprocess()
    print type(s)
    print
    print isinstance(s,shutdownNow)
    print isinstance(s,shutdownMicroprocess)
    print isinstance(s,shutdown)
    print
    
