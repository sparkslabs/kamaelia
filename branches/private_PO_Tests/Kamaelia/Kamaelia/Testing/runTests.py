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

import os
import new
import test
import unittest
import sys
import glob

def get_suites():
	dir = os.path.dirname(os.path.abspath(sys.modules[__name__].__file__))
	suites = []
	for testFile in glob.glob(dir + os.sep + 'test/test_*.py'):
		testModuleName = os.path.basename(testFile)[:-len('.py')]
		testModule = __import__('test.' + testModuleName,globals(),locals(),[testModuleName])
		if hasattr(testModule,'suite') and callable(testModule.suite):
			suites.append(testModule.suite())
	return suites

def suite():
	suites = get_suites()
	suite = unittest.TestSuite(suites)
	return suite

def runGui():
	import unittestgui
	unittestgui.main(__name__ + '.suite')

def runConsole():
	sys.argv = [sys.argv[0]]
	unittest.main(defaultTest = 'suite')

#DEFAULT_UI = 'gui'
DEFAULT_UI = 'console' 

if __name__ == '__main__':
	if len(sys.argv) == 1:
		ui = DEFAULT_UI
	else:
		ui = sys.argv[1]

	if ui == 'console':
		runConsole()
	elif ui == 'gui':
		runGui()
	else:
		print >>sys.stderr, "Select ui [console|gui]"
