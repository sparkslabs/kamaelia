#!/usr/bin/env python
#
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
# -------------------------------------------------------------------------
"""\
See Axon.Base
"""

class AxonType(type):
   """\
   Metaclass for Axon objects.
   """
    
   def __init__(cls, name, bases, dict):
      """\
      Override creation of class to set a 'super' attribute to what you get
      when you call super().

      **Note** that this 'super' attribute is deprecated - there are some subtle
      issues with it and it should therefore be avoided.
      """
      super(AxonType, cls).__init__(name, bases, dict)
      setattr(cls, "_%s__super" % name, super(cls))

class AxonObject(object):
   """\
   Base class for axon objects.

   Uses AxonType as its metaclass.
   """
   __metaclass__ = AxonType
   pass

