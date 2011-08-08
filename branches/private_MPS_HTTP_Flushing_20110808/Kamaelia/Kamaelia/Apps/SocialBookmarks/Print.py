
import sys

def Print(*args):
    for arg in args:
        try:
            x = str(arg)
        except:
            pass
        try:
            print x,
        except: 
            try:
                print unicode(x, errors="ignore"),
            except: 
                try:
                    sys.stdout.write(arg.encode("ascii","ignore"))
                except:
                        print "FAILED PRINT"
    print
