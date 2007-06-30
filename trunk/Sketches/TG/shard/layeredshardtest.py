from shard import *

"""
Test case to check that adding shards to shards doesn't cause
any circularity problems, e.g. required methods loops, etc.

Results:
- Requirements lists cause no problems
- Any class can be used as a shard
- Dependency calculation when combining shards/classes in
  either order gives the same result IF both shard and target
  container class declare their requirements
"""

# class: requires c; provides a
class t1(object):
    def a(self):
        self.c()

# shard: requires a, b; provides c, d
class s1(object):
    def c(self):
        print 's1: c'
        self.b()
    
    def d(self):
        print 's1: d'
    
    def needsa(self):
        self.a()

# shard: requires d; provides b
class s2(object):
    def b(self):
        self.d()

# shard: requires b; provides d
class s3(object):
    def s3(self):
        self.b()
    
    def d(self):
        print 's3: d'

requires('a', 'b')(s1)
requires('d')(s2)
requires('b')(s3)

addShards(s2)(s3)
s3().s3()

# same dependency flagged whichever way round shards combined
#addShards(s2)(s1)
#addShards(s1)(s2)

addShards(s1, s2)(t1)
t1().a()
t1().d()
t1().b()