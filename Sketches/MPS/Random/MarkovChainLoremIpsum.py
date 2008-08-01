#!/usr/bin/python

import pprint
import random

f = open("pandp12.txt","r")
lines = []
for line in f:
    lines.append(line)

f.close()

s = "".join(lines)
s.lower()    

s = s.replace("\r","")
s = s.replace("\n"," ")

followset = {

}

chain = 1

current = [x for x in " "+s[:chain]]
# print current

for i in s[chain:]:
    try:
        followset[tuple(current)].append(i)
    except KeyError:
        followset[tuple(current)] = [ i ]
    current = current[1:]
    current.append(i)

word_starts = [ x for x in followset.keys() if x[0] == " "]

X = list(random.choice(word_starts))

R = []
spaces = 0
lines = 0
linelen = 0
while lines<100:
    linelen += 1
    R.append(X[0])
    try:
        FS = followset[tuple(X)]
    except KeyError:
        Y = [x for x in "".join(X).replace("\n"," ")]
        FS = followset[tuple(Y)]
        
    next = random.choice(FS)
    if next == " ":
        spaces +=1
        if spaces > 14:
            if linelen > 60:
#                print ">>>>>>>>>>>>>>", linelen
                next = "\n"
                lines +=1
                spaces = 0
                linelen = 0
    X = X[1:]+[next]

#    X = (X[1], X[2], X[3], next)
    

print "".join(R[1:])

# print repr("".join(R[1:]))

