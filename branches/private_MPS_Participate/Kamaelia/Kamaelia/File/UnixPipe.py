"""\
This is a deprecation stub, due for later removal.
"""

import Kamaelia.Support.Deprecate as Deprecate
from Kamaelia.File.UnixProcess import UnixProcess as __UnixProcess

Deprecate.deprecationWarning("Use Kamaelia.File.UnixProcess instead of Kamaelia.File.UnixPipe")

Pipethrough = Deprecate.makeClassStub(
    __UnixProcess,
    "Use Kamaelia.File.UnixProcess:UnixProcess instead of Kamaelia.File.UnixPipe:Pipethrough",
    "WARN"
    )

# def __foo(*larg, **darg):
#     return __Pipeline(*larg,**darg)
#
# foo = Deprecate.makeFuncStub(__foo, message="blob")
