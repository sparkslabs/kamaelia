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

import libraries

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
