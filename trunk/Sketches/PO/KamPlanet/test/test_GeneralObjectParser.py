#!/usr/bin/env python
# -*- coding: utf-8 -*-
#-*-*- encoding: utf-8 -*-*-
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
# Licensed to the BBC under a Contributor Agreement: PO

"""
The tests in this file could be implemented with unittest instead of with KamTestCase. The point 
is to have some tests that are 100% compatible with unittest. While this might sound obvious 
since KamTestCase *currently* inherits unittest.TestCase, maybe in a short future this is changed
somehow (i.e. not using inheritance but delegation), and these tests still need to be compatible.
"""

import Kamaelia.Testing.KamTestCase as KamTestCase

from GeneralObjectParser import GeneralObjectParser, Field

class GeneralObjectParserTestCase(KamTestCase.KamTestCase):
    def testSimpleGeneralObjectParser(self):
        generalObjectParser = GeneralObjectParser(
                    field1 = Field(int, 5),
                    field2 = Field(str, 'mydefaultvalue'),
                )
        generalObjectParser.field1.parsedValue += "31"
        obj = generalObjectParser.generateResultObject()
        self.assertEquals(31, obj.field1)
        self.assertEquals('mydefaultvalue', obj.field2)
        
    def testErroneousGeneralObjectParser(self):
        generalObjectParser = GeneralObjectParser(
                    field1 = Field(int, 5),
                    field2 = Field(str, 'mydefaultvalue'),
                )
        generalObjectParser._VERBOSE = False
        generalObjectParser.field1.parsedValue += "this.is.not.an.int"
        obj = generalObjectParser.generateResultObject()
        self.assertEquals(5, obj.field1)
        self.assertEquals('mydefaultvalue', obj.field2)
    
def suite():
    return KamTestCase.makeSuite(GeneralObjectParserTestCase.getTestCase())
    
if __name__ == '__main__':
    KamTestCase.main(defaultTest='suite')
