#!/usr/bin/python

import sys
import os
import inspect
import time

import Axon

# This means the file defaults to print, unless the PrintOnFile component is active
# Also means that it fails to ON, rather than failing to OFF.
doPrint = True 

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
    if doPrint:
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
                sys.stdout.write( x )
            except: 
                try:
                    sys.stdout.write( unicode(x, errors="ignore") )
                except: 
                    try:
                        sys.stdout.write(arg.encode("ascii","ignore"))
                    except:
                            print ("FAILED PRINT")
        print
        sys.stdout.flush()

class PrintOnFile(Axon.ThreadedComponent.threadedcomponent):
    "Class to make printing of messages conditional"
    printfile = "/tmp/doPrint"
    def main(self):
        global doPrint
        c = 0
        while True:
            if os.path.exists(self.printfile):
                doPrint = True
            else:
                doPrint = False
            time.sleep(10)

if __name__ == "__main__":
    class Printer(Axon.ThreadedComponent.threadedcomponent):
        def main(self):
            while True:
                Print("Test")
                time.sleep(1)

    PrintOnFile().activate()
    Printer().run()
