
import sys
import os
import inspect
import time

def __LINE__ ():
    caller = inspect.stack()[1]
    return int (caller[2])
     
def __FUNC__ ():
    caller = inspect.stack()[1]
    return caller[3]

def __BOTH__():
    caller = inspect.stack()[1]
    return int (caller[2]), caller[3], caller[1]

def Print(*args):
    caller = inspect.stack()[1]
    filename = str(os.path.basename(caller[1]))
    sys.stdout.write(filename+ " : "+ str(int (caller[2])) + " : ")
    sys.stdout.write(str(time.time()) + " : ")
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
    sys.stdout.flush()
