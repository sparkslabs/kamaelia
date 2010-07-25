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
from Shard import *
from CDrawing import *
from cshard import getshard

## shard
# from function
s = shard(function = drawBG)
for line in s.code:
    print line,
print s.name
print

# from code
s = shard(code = getshard(drawBG))
for line in s.code:
    print line,
print s.name
print

s = shard(name = "drawBG", code = getshard(drawBG))
for line in s.code:
    print line,
print s.name
print

# mix
s = shard(name = "drawBG", code = getshard(drawBG))
ss = shard(name = 'test', annotate = True, shards = [blitToSurface, s])
for line in ss.code:
    print line,
print ss.name
print

s = shard(name = "drawBG", code = getshard(drawBG))
ss = shard(name = 'test', annotate = True, shards = [blitToSurface, s])
sss = shard(annotate = True, shards = [blitToSurface, s, ss])
for line in sss.annotate():
    print line,
print

## classShard
from ClassShard import *
cs = classShard('classtest', docstring = 'docstring', shards = [s, ss])
for l in cs.code:
    print l,
print

## functionShard
from FunctionShard import *
fs = functionShard('functest', shards = [drawBG, s, ss], docstring = 'comment here')
for l in fs.code:
    print l,
print

## moduleShard
from ModuleShard import *
imps = ['lala', 'doo', 'ming']
impfrs = {'wheee': ['huphup', 'pop', 'pip'], 'nanoo': ('noom', )}
ms = moduleShard('moduletest', importmodules = imps, importfrom = impfrs, shards = [fs], docstring = 'module doc')
for l in ms.code:
    print l,
print

## funcAppShard
from FuncAppShard import *
ps = ['lala', 'doo', 'ming']
kws = {'wheee': "[huphup, 'pop', 'pip', 1]", 'nanoo': '"noom"', 'a': '1'}
app = funcAppShard('testcall', funcObj = None, args = ps, kwargs = kws)
for ln in app.code:
    print ln,
print
app = funcAppShard('testcall', funcObj = 'testobj', args = ps, kwargs = kws)
for ln in app.code:
    print ln,
print