"""Module for partial classes.

To declare a class partial, inherit from partial.partial and from
the full class, like so

from partial import *
import original_module

class ExtendedClass(partial, original_module.FullClass):
    def additional_method(self, args):
        body
    more_methods

After this class definition is executed, original_method.FullClass
will have all the additional properties defined in ExtendedClass;
the name ExtendedClass is of no importance (and becomes an alias
for FullClass),
It is an error if the original class already contains the 
definitions being added, unless they are methods declared
with @replace.
"""

class MetaPartial(type):
    "Metaclass implementing the hook for partial class definitions."
    
    # attributes that shouldn't be overwritten
    ignoreList = ['__module__', '__doc__', '__metaclass__']

    def __new__(mcls, name, bases, dict):
        if not bases:
            # It is the class partial itself
            return type.__new__(mcls, name, bases, dict)
        if len(bases) != 2:
            raise TypeError, "A partial class definition must have only one base class to extend"
        base = bases[1]
        for k, v in dict.items():
            if k in mcls.ignoreList:
                # Ignore implicit attribute
                continue
            if k in base.__dict__ and not hasattr(v, '__replace'):
                raise TypeError, '%s already has %s' % (repr(base), k)
            setattr(base, k, v)
            #base.__dict__[k] = v    # this can cause TypeError: Error when calling the metaclass bases 'dictproxy' object does not support item assignment
        # Return the original class
        return base

class partial:
    "Base class to declare partial classes. See module docstring for details."
    __metaclass__ = MetaPartial

def replace(f):
    """Method decorator to indicate that a method shall replace 
    the method in the full class."""
    f.__replace = True
    return f

