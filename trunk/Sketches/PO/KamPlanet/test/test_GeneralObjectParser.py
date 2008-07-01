#!/usr/bin/env python
#-*-*- encoding: utf-8 -*-*-
# 
# (C) 2008 British Broadcasting Corporation and Kamaelia Contributors(1)
#     All Rights Reserved.
#
# You may only modify and redistribute this under the terms of any of the
# following licenses(2): Mozilla Public License, V1.1, GNU General
# Public License, V2.0, GNU Lesser General Public License, V2.1
#
# (1) Kamaelia Contributors are listed in the AUTHORS file and at
#     http://kamaelia.sourceforge.net/AUTHORS - please extend this file,
#     not this notice.
# (2) Reproduced in the COPYING file, and at:
#     http://kamaelia.sourceforge.net/COPYING
# Under section 3.5 of the MPL, we are using this text since we deem the MPL
# notice inappropriate for this file. As per MPL/GPL/LGPL removal of this
# notice is prohibited.
#
# Please contact us via: kamaelia-list-owner@lists.sourceforge.net
# to discuss alternative licensing.
# -------------------------------------------------------------------------
# Licensed to the BBC under a Contributor Agreement: PO

"""
The tests in this file could be implemented with unittest instead of with KamTestCase. The point 
is to have some tests that are 100% compatible with unittest. While this might sound obvious 
since KamTestCase *currently* inherits unittest.TestCase, maybe in a short future this is changed
somehow (i.e. not using inheritance but delegation), and these tests still need to be compatible.
"""

import kamtest.KamTestCase as KamTestCase

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
