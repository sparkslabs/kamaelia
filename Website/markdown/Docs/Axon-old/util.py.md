---
pagename: Docs/Axon-old/util.py
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
[Axon.]{style="font-size:24pt"}[util.py]{style="font-size:24pt;font-weight:600"}

Version: Axon 1.0

Selection of utility functions and classes. (All highly trivial)

[TODO:]{style="font-weight:600"} Fix test suite doc strings for auto
testdocs

[Pydoc Style Documentation]{style="font-size:14pt;font-weight:600"}

[CLASSES]{style="font-weight:600"}

class Finality(exceptions.Exception)

-   Used for implementing try\...finally\... inside a generator

[FUNCTIONS]{style="font-weight:600"}

[axonRaise(someException, \*args)]{style="font-weight:600"}

[listSubset(requiredList, suppliedList)]{style="font-weight:600"}

[logError(someException, \*args)]{style="font-weight:600"}

-   Currently does nothing but can be rewritten to log ignored errors if
    the production value is true.

[removeAll(xs, y)]{style="font-weight:600"}

-   Very simplistic method of removing all occurances of y in list xs.

[safeList(arg=None)]{style="font-weight:600"}

[testInterface(theComponent, interface)]{style="font-weight:600"}

Look for a minimal match interface for the component

[DATA]{style="font-weight:600"}

production = False

[Testdoc Documentation]{style="font-size:14pt;font-weight:600"}

[Finality]{style="font-weight:600"}

-   dummy class deriving from Exception - used for implementing
    try\...finally in a generator

[axonRaise]{style="font-weight:600"}

-   behaviour depends on the value of production. If true it will simply
    return False. Otherwise it will throw an exception of the type
    passed to it with the other arguments passed to the constructor.

[listSubset]{style="font-weight:600"}

-   returns true if the first list argument is a subset of the second
    list argument

[logError]{style="font-weight:600"}

-   At the moment this function does nothing but can be rewritten to log
    ignored exception data. Equally the test does nothing.

[production]{style="font-weight:600"}

-   Is a module value that turns off some exception to make the system
    tolerant of failure when running in production. For development and
    testing it should be False to allow uncaught exceptions to bring
    down the system.

[removeAll - (xs:list,y)]{style="font-weight:600"}

-   removes all occurances of y from the list xs.

[safeList]{style="font-weight:600"}

-   always returns a list even if the arg for constructing the list
    would normally cause a typeerror.

[safeList]{style="font-weight:600"}

-   Like list it returns an empty list when called without an argument.

[safeList]{style="font-weight:600"}

-   Returns an empty list if the argument would cause a TypeError if
    passed to list(). That is anything without an iterator method.

[testInterface]{style="font-weight:600"}

-   returns true for a \_minimal match\_ on the interface of the
    component
-   In production mode failed tests will return false. Otherwise they
    will throw an exception that is likely to stop the system.

Michael, December 2004
