#!/usr/bin/python

print "0. Generators"
print "You're expected to manually copy and paste the contents"
print "of this file into a python console, so you can see what"
print "it does"

def fib(a,b):
    while 1:
        yield a
        a, b = b, b + a

g = fib(1,1)
g
g.next()
g.next()
g.next()
g.next()
g.next()
g.next()

GS = [ fib(x,x) for x in range(10) ]
GS
[ G.next() for G in GS ]
[ G.next() for G in GS ]
[ G.next() for G in GS ]
[ G.next() for G in GS ]
[ G.next() for G in GS ]
[ G.next() for G in GS ]

def fib(a,b):
    while 1:
        yield 1 # Just to say "keep running me"
        print a
        a, b = b, b + a

g = fib(1,1)
g
for i in range(15):
    r = g.next()

def printer(tag):
    while 1:
        yield 1 # Makes it a generator
        print tag

PS = [ printer(str(x)) for x in range(10) ]
PS
for i in range(10):
    r = [ p.next() for p in PS ]

print
print
print "0. Generators"
print "You're expected to manually copy and paste the contents"
print "of this file into a python console, so you can see what"
print "it does"
