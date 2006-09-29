#!/usr/bin/env python

# a little experiment with adding traceback output to deprecation warnings,
# to assist the developer.

# NB: Removes last item from the stack trace - since that is within the stub,
#     which is of no interest to the developer.

"""\
This is a deprecation stub, due for later removal.

See Kamaelia.Chassis.Pipeline instead.
"""


import Deprecate
from Kamaelia.Chassis.Pipeline import Pipeline as __Pipeline

Deprecate.deprecationWarning("Use Kamaelia.Chassis.Pipeline instead of Deprecation")

pipeline = Deprecate.makeClassStub(
    __Pipeline,
    "Use Kamaelia.Chassis.Pipeline:Pipeline instead of Deprecation:pipeline."
    )

# def __foo(*larg, **darg):
#     return __Pipeline(*larg,**darg)
# 
# foo = Deprecate.makeFuncStub(__foo, message="blob")
