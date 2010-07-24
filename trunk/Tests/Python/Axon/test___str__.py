#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
#
# Tests __str__ for different classes
#

import unittest

class str_Test(unittest.TestCase):
   classtotest=None

   def test___str__(self):
      if not self.__class__ is str_Test:
         a = self.__class__.classtotest()
         b = self.__class__.classtotest()
         self.failIf(str(a)==str(b), "str does not produce a result unique to" + self.__class__.classtotest.__name__ +" instance.")
         self.failUnless(str(a)==str(a),"str does not produce a consistent result")

