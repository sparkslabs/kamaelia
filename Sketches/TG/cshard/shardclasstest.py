from Shard import *
from CDrawing import *
from cshard import getshard

#~ # from function
#~ s = shard(function = drawBG)
#~ for line in s.code:
#~     print line,
#~ print s.name
#~ print

#~ # from code
#~ s = shard(code = getshard(drawBG))
#~ for line in s.code:
#~     print line,
#~ print s.name
#~ print

#~ s = shard(name = "drawBG", code = getshard(drawBG))
#~ for line in s.code:
#~     print line,
#~ print s.name
#~ print

#~ # mix
#~ s = shard(name = "drawBG", code = getshard(drawBG))
#~ ss = shard(name = 'test', annotate = True, shards = [blitToSurface, s])
#~ for line in ss.code:
#~     print line,
#~ print ss.name
#~ print

s = shard(name = "drawBG", code = getshard(drawBG))
ss = shard(name = 'test', annotate = True, shards = [blitToSurface, s])
sss = shard(annotate = True, shards = [blitToSurface, s, ss])
#~ for line in sss.annotate():
#~     print line,
#~ print

## classShard
from ClassShard import *

cs = classShard('classtest', shards = [s, ss])
for l in cs.code:
    print l,
print
