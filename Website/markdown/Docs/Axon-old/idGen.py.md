---
pagename: Docs/Axon-old/idGen.py
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
[Axon.]{style="font-size:24pt"}[idGen.py]{style="font-size:24pt;font-weight:600"}

Version: Axon 1.0

idGen() - idsequence generator

[Pydoc Style Documentation]{style="font-size:14pt;font-weight:600"}

[FUNCTIONS]{style="font-weight:600"}

[newId = strId(self, thing) method of idGen
instance]{style="font-weight:600"}

-   \'IG.strId(object)\' - Allocates & returns the next available id
    combined with the object\'s class name, in string form

[numId(self) method of idGen instance]{style="font-weight:600"}

-   \'IG.numId()\' - Allocates & returns the next available id

[strId(self, thing) method of idGen instance]{style="font-weight:600"}

-   \'IG.strId(object)\' - Allocates & returns the next available id
    combined with the object\'s class name, in string form

[tupleId(self, thing) method of idGen instance]{style="font-weight:600"}

-   \'IG.tupleId(thing)\' -\> (IG.numId(), IG.strId(thing)), but with
    ids the same in num & str

class idGen(object)

Methods defined here:

[idToString(self, thing, aNumId)]{style="font-weight:600"}

-   [INTERNAL]{style="font-style:italic;font-weight:600"}
    \'IG.idToString(thing,numId)\' - Combines the \'str()\' of the
    object\'s class with the id to form a string id

[next = nextId(self)]{style="font-weight:600"}

[nextId(self)]{style="font-weight:600"}

-   [INTERNAL]{style="font-style:italic;font-weight:600"}
    \'IG.nextId()\' - returns the next id, incrementing the private
    class variable

[numId(self)]{style="font-weight:600"}

-   \'IG.numId()\' - Allocates & returns the next available id

[strId(self, thing)]{style="font-weight:600"}

-   \'IG.strId(object)\' - Allocates & returns the next available id
    combined with the object\'s class name, in string form

[tupleId(self, thing)]{style="font-weight:600"}

-   \'IG.tupleId(thing)\' -\> (IG.numId(), IG.strId(thing)), but with
    ids the same in num & str

\...

[Testdoc Documentation]{style="font-size:14pt;font-weight:600"}

[TODO: ]{style="font-weight:600"}Implement test suite for Axon.debug.py
(We did mention that tests were added late in the project?)

Michael, December 2004
