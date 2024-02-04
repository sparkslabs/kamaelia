---
pagename: PyrexComponents
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
[Using Pyrex To Write
Components]{style="font-size:24pt;font-weight:600"}

First stab at writing Kamaelia Components using Pyrex. This code uses
Pyrex 0.9.3, and has some issues that need resolving, but this does
actually work.

[File: pyrexcomponent.pyx]{style="font-size:14pt;font-weight:600"}

<div>

[\#\
\# Simple pyrex component\
\#\
\
import Axon.Component.component\
\
cdef class test(Axon.Component.component):]{style="font-family:Courier"}

</div>

<div>

[def mainBody(self):]{style="font-family:Courier"}

</div>

<div>

[if self.dataReady(\"inbox\"):]{style="font-family:Courier"}

</div>

<div>

[return 1]{style="font-family:Courier"}

</div>

[File: Axon.Component.pxd]{style="font-size:14pt;font-weight:600"}

<div>

[class component:]{style="font-family:Courier"}

</div>

[File: setup.py]{style="font-size:14pt;font-weight:600"}

<div>

[from distutils.core import setup\
from distutils.extension import Extension\
from Pyrex.Distutils import build\_ext\
\
setup(]{style="font-family:Courier"}

</div>

::: {dir="ltr"}
[name = \'PyrexComponent\',]{style="font-family:Courier"}
:::

::: {dir="ltr"}
[ext\_modules=list(]{style="font-family:Courier"}
:::

::: {dir="ltr"}
[Extension(\"pyrexcomponent\",]{style="font-family:Courier"}
:::

::: {dir="ltr"}
[),]{style="font-family:Courier"}
:::

::: {dir="ltr"}
[ ),]{style="font-family:Courier"}
:::

::: {dir="ltr"}
[cmdclass = {\'build\_ext\': build\_ext}]{style="font-family:Courier"}
:::

::: {dir="ltr"}
[)]{style="font-family:Courier"}
:::

[Build]{style="font-size:14pt;font-weight:600"}

[Creating an instance]{style="font-size:14pt;font-weight:600"}

[Summary]{style="font-size:14pt;font-weight:600"}

There\'s clearly some minor issues here and scope for improvement, but
this clearly shows that you [can]{style="font-style:italic"} write
components in pyrex, which therefore means you can pull in any library
with a C interface with relative ease.
