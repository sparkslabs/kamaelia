---
pagename: Docs/Axon-old/Axon.py
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
[Axon.]{style="font-size:24pt"}[Axon.py]{style="font-size:24pt;font-weight:600"}

Version: Axon 1.0

Defines a metaclass that allows super class calling in a slightly nicer
manner in terms of syntactic sugar/easier to get right that still has
the good effects of \"super\" in a multiple inheritance scenario.

[Pydoc Style Documentation]{style="font-size:14pt;font-weight:600"}

[Testdoc Documentation]{style="font-size:14pt;font-weight:600"}

[AxonObject]{style="font-weight:600"}

-   derives from object, but sets a metaclass of AxonType - to allow
    superclass method calling simply. ttbChecked

[AxonType.\_\_init\_\_]{style="font-weight:600"}

-   adds an extra \_\_super method to all objects created from classes
    with this metaclass simplifying superclass method calling.
    ttbChecked

..

Michael, December 2004
