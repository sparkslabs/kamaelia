#!/usr/bin/python

import pprint
import dirac
import dirac.dirac_parser

print "---------------------------------"
print "dirac.version ==", dirac.version
print "dirac.dirac_parser.version ==", dirac.dirac_parser.version
print "dirac.dirac_parser.NUM_WLT_FILTERS ==", dirac.dirac_parser.NUM_WLT_FILTERS
assert ( dirac.version == (1, 0, 2) )
assert ( dirac.dirac_parser.version == (1, 0, 2) )
assert ( dirac.dirac_parser.NUM_WLT_FILTERS == 8 )

# print "dir(dirac)"
# pprint.pprint( dir(dirac) )

# print "---------------------------------"
# print "dir(dirac.dirac_parser)"
# pprint.pprint( dir(dirac.dirac_parser) )
# print "---------------------------------"

def fileReader(filename="/home/kamaelian/foo.drc"):
    f = open("/home/kamaelian/foo.drc")
    while True:
        data = f.read(8192)
        if data:
            yield data
        else:
            return
 
d = dirac.dirac_parser.DiracDecoder()
f = fileReader()
# print "dir(d)", d
# pprint.pprint( dir(d) )

print "VERBOSE", d.verbose()
display_it = True
fc = 0
try:
    while True:
        try:
            F = d.getFrame()
            fc += 1
            if display_it:
                del F["yuv"]
                print "FRAME:", pprint.pformat(F).replace("\n", "\n       ")
        except dirac.dirac_parser.DiracDecodeException, e:
            reason, help =  e.args
            if reason == "STATE_BUFFER":
                print "Did not get frame because of", reason
                print "We now ought to do this"
                print help
                data = f.next()
                print "GOT DATA", len(data)
                print "Buffering Data"
                d.bufferData( data )
            elif reason == "STATE_SEQUENCE":
                print "STATE_SEQUENCE"
                pprint.pprint(d.SourceParams())
            else:
                print "HMM"
                break
except StopIteration:
    pass

print "Frame Count", fc

# STATE_BUFFER









