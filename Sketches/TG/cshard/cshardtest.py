from cshard import *

"""
Code generation testing
"""

#~ # importmodules
imps = importmodules('lala', 'doo', 'ming', wheee = ['huphup', 'pop', 'pip'], nanoo = ('noom', ))
for line in imps:
    print line,

#~ # setindent
impsind = setindent(imps, level = 1)
for line in impsind:
    print line,

impsind = setindent(imps, level = 2)
for line in impsind:
    print line,

impsind = setindent(impsind)
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
