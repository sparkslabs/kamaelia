#!/usr/bin/env python

# a little experiment with adding traceback output to deprecation warnings,
# to assist the developer.

# NB: Removes last item from the stack trace - since that is within the stub,
#     which is of no interest to the developer.

"""\
This is a deprecation stub, due for later removal.

See Kamaelia.Chassis.Pipeline instead.
"""

from Kamaelia.Chassis.Pipeline import Pipeline as __Pipeline

class pipeline(__Pipeline):
    def __init__(self, *larg, **darg):
        import sys, traceback
        sys.stderr.write('***DEPRECATION WARNING***\n')
        sys.stderr.write('Use "Kamaelia.Chassis.Pipeline.Pipeline" instead of "Kamaelia.Util.Pipeline.pipeline"\n')
        sys.stderr.write(''.join(traceback.format_list(traceback.extract_stack()[:-1])))
        super(pipeline,self).__init__(*larg,**darg)

class Pipeline(__Pipeline):
    def __init__(self, *larg, **darg):
        import sys, traceback
        sys.stderr.write('***DEPRECATION WARNING***\n')
        sys.stderr.write('Use "Kamaelia.Chassis.Pipeline.Pipeline" instead of "Kamaelia.Util.Pipeline.Pipeline"\n')
        sys.stderr.write(''.join(traceback.format_list(traceback.extract_stack()[:-1])))
        super(Pipeline,self).__init__(*larg,**darg)

if __name__=="__main__":
    raise DeprecationWarning("This is a stub. See Kamaelia.Chassis.Pipeline instead.")
