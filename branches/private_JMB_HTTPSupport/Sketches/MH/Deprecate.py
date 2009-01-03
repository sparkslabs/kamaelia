#/usr/bin/env python



# levels: 
#  "" | "SILENT"  - supresses all deprecation warnings
#  "FIRST"        - display warning only for first usage of each deprecated entity
#  "TRACE"        - displays warning for all deprecations, including traceback for each
#  "RAISE"        - raises exception

import os

GLOBAL_WARNING_LEVEL = os.environ.get("KAMAELIA_DEBUG","SILENT")

import sys,traceback


def makeClassStub(klass, message, warninglevel="SILENT"):
    """\
    makeClasStub(klass, message[, warninglevel]) -> stub for target klass.
    
    Returns a stub class for the specified target class. The stub will output
    deprecation warnings in accordance with the higher of the specified warning
    level and the system wide one.
    """
    class stub(klass):
        __warn       = Warning("DEPRECATED: "+message, warninglevel)
        
        def __init__(self, *larg, **darg):
            stub.__warn(chopTrace=2)
            super(stub,self).__init__(*larg, **darg)
                
    return stub

def makeFuncStub(target, message, warninglevel="SILENT"):
    """\
    makeFuncStub(func, message[, warninglevel]) -> stub for target func.
    
    Returns a stub function for the specified target func. The stub will output
    deprecation warnings in accordance with the higher of the specified warning
    level and the system wide one.
    """
    def stub(*larg, **darg):
        stub.__warn(chopTrace=2)
        return func(*larg, **darg)
    
    stub.__warn       = Warning("DEPRECATED: "+message, warninglevel)
    return stub

def deprecationWarning(message, warninglevel="SILENT"):
    """\
    deprecationWarning(message[, warninglevel]) -> display deprecation warning.
    
    Outputs a deprecation warning in accordance with the higher of the specified
    warning level and the system wide one.
    """
    return Warning("DEPRECATED: "+message, warninglevel)(chopTrace=3)


class Warning(object):
    """\
    Warning(message[, warninglevel]) -> new callable Warning object.
    
    Implements warning mechanisms. When called, will output warnings according
    to the set warning level. The warning level used will be the greater of the
    specified one and the system wide level.
    """
    def __init__(self, message, warninglevel="SILENT"):
        super(Warning,self).__init__()
        self.message = message
        
        self._warn   = False
        self._repeat = False
        self._trace  = False
        self._crash  = False
        self.setLevel(GLOBAL_WARNING_LEVEL)
        self.setLevel(warninglevel)
        
    def setLevel(self, level):
        level = level.strip().upper()
        if level == "FIRST":
            self._warn   = True
        elif level == "TRACE":
            self._warn   = True
            self._repeat = True
            self._trace  = True
        elif level == "RAISE":
            self._warn   = True
            self._repeat = True
            self._trace  = True
            self._crash  = True
        return self
        
    def __call__(self,chopTrace=1):
        if self._warn:
            sys.stderr.write(self.message+"\n")
            if not self._repeat:
                self._warn=False
        if self._crash:
            raise DeprecationWarning()
        if self._warn and self._trace:
            sys.stderr.write(''.join(traceback.format_list(traceback.extract_stack()[:-chopTrace])))


