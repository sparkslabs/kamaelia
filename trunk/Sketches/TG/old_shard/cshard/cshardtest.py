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
from cshard import *

"""
Code generation testing
"""

#~ # importmodules
imps = importmodules('lala', 'doo', 'ming', wheee = ['huphup', 'pop', 'pip'], nanoo = ('noom', ))
for line in imps:
    print line,

#~ # setindent

impsind = indent(imps, level = 0)
for line in impsind:
    print line,

impsind = indent(imps, level = 1)
for line in impsind:
    print line,

impsind = indent(imps, level = 2)
for line in impsind:
    print line,

impsind = indent(impsind, level = -1)
for line in impsind:
    print line,

impsind = indent(impsind)
for line in impsind:
    print line,

#~ # makeclass
for line in makeclass("CMagnaDoodle"):
    print line,
for line in makeclass("CMagnaDoodle", []):
    print line,
for line in makeclass("CMagnaDoodle", ['Axon.Component.component']):
    print line,
for line in makeclass("CMagnaDoodle", ['Axon.Component.component', 'dummy']):
    print line,

#~ # makedoc
doc = "one line doc"
docs = makedoc(doc)
for line in docs:
    print line,

doc = "manymany\nline\ndoc\ndoo doo doo"
docs = makedoc(doc)
for line in docs:
    print line,

#~ # makeboxes
for line in makeboxes():
    print line,
print

for line in makeboxes(True, False):
    print line,
print

for line in makeboxes(inboxes = False, default = True):
    print line,
print

for line in makeboxes(inboxes = True, default = False, doo = "useless box", dum = "twin"):
    print line,
print

for line in makeboxes(True, True, doo = "useless box", dum = "twin"):
    print line,
print

#~ # getshard
from CDrawing import *

for line in getshard(drawBG):
    print line,
print

for line in getshard(drawBG, 2):
    print line,
print

for line in getshard(drawBG, 0):
    print line,
print

for line in getshard(blitToSurface, 3):
    print line,
print

for line in getshard(displaySetup):
    print line,
print

#~ # annotateshard
from CDrawing import *
for line in annotateshard(getshard(drawBG), "drawBG"):
    print line,
print

for line in annotateshard(getshard(drawBG, 2), 'pop', 2):
    print line,
print

for line in annotateshard(getshard(drawBG, 0), 'drawBG', 0, delimchar='='):
    print line,
print

for line in annotateshard(getshard(blitToSurface, 3), 'bts', delimchar='e'):
    print line,
print

for line in annotateshard(getshard(displaySetup), ""):
    print line,
print

#~ # makearglist
args = ['la', 'hmm']
kwargs = {'pop':'True', 'num':'1'}
print makearglist([], kwargs)
print makearglist(args, None)
print makearglist(args, kwargs, exarg = 'args')
print makearglist(None, kwargs, exkwarg = 'kwargs')
print makearglist(args, {}, exarg = 'args', exkwarg = 'kwargs')
print

#~ # makefunction (incomplete...)
args = ['la', 'hmm']
kwargs = {'pop':'True', 'num':'1'}
name = 'fun'
print makefunction(name, args, kwargs, exkwarg = 'kwargs')
