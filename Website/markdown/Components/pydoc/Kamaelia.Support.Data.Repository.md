---
pagename: Components/pydoc/Kamaelia.Support.Data.Repository
last-modified-date: 2009-06-05
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
[Kamaelia](/Components/pydoc/Kamaelia.html){.reference}.[Support](/Components/pydoc/Kamaelia.Support.html){.reference}.[Data](/Components/pydoc/Kamaelia.Support.Data.html){.reference}.[Repository](/Components/pydoc/Kamaelia.Support.Data.Repository.html){.reference}
=========================================================================================================================================================================================================================================================================
:::

::: {.section}
::: {.container}
:::

-   [Kamaelia component repository introspection](#42){.reference}
    -   [Example Usage](#43){.reference}
        -   [Simple lists of component/prefab names](#44){.reference}
        -   [Detailed introspections::](#45){.reference}
    -   [Obtaining introspection data](#46){.reference}
    -   [How are components and prefabs detected?](#47){.reference}
    -   [Structure of detailed introspections](#48){.reference}
    -   [Implementation Details](#49){.reference}
:::

::: {.section}
Kamaelia component repository introspection {#42}
===========================================

This support code scans through a Kamaelia installation detecting
components and picking up relevant information such as doc strings,
initializer arguments and the declared Inboxes and Outboxes.

It not only detects components and prefabs, but also picks up modules,
classes and functions - making this a good source for documentation
generation.

::: {.section}
[Example Usage]{#example-usage} {#43}
-------------------------------

::: {.section}
### [Simple lists of component/prefab names]{#simple-lists-of-component-prefab-names} {#44}

Fetch a flat listing of all components. The key is the module path (as a
tuple) and the value is a list of the names of the components found:

``` {.literal-block}
>>> r=Repository.GetAllKamaeliaComponents()
>>> r[('Kamaelia','Util','Console')]
['ConsoleEchoer', 'ConsoleReader']
```

Fetch a *nested* listing of all components. The leaf is a list of entity
names:

``` {.literal-block}
>>> r=Repository.GetAllKamaeliaComponentsNested()
>>> r['Kamaelia']['Util']['Console']
['ConsoleEchoer', 'ConsoleReader']
```

Fetch a flat listing of all prefabs:

``` {.literal-block}
>>> p=Repository.GetAllKamaeliaPrefabs()
>>> p[('Kamaelia','File','Reading')]
['RateControlledFileReader', 'RateControlledReusableFileReader',
'ReusableFileReader', 'FixedRateControlledReusableFileReader']
```

Fetch a *nested* listing of all prefabs:

``` {.literal-block}
>>> p=Repository.GetAllKamaeliaPrefabsNested()
>>> p['Kamaelia']['File']['Reading']
['RateControlledFileReader', 'RateControlledReusableFileReader',
'ReusableFileReader', 'FixedRateControlledReusableFileReader']
```

Fetching a flat listing of components as defined in a specific directory
(rather than the current Kamaelia installation):

``` {.literal-block}
>>> r=Repository.GetAllKamaeliaComponents(baseDir="/data/my-projects/my-components/")
```
:::

::: {.section}
### [Detailed introspections::]{#detailed-introspections} {#45}

We can ask for a complete introspection of the current Kamaelia
installation:

``` {.literal-block}
>>> docTree=Repository.ModuleDoc("Kamaelia","/usr/lib/python/site-packages/Kamaelia")
>>> docTree.resolve(roots={"Kamaelia":docTree})
```

And look up a particular module:

``` {.literal-block}
 >>> m=docTree.find("Util.Console")
 >>> m
<Repository.ModuleDoc object at 0x40403b0c>
```

Then find components declared in that module:

``` {.literal-block}
>>> cs=m.listAllComponents()
>>> cs
[('ConsoleReader', <Repository.ClassScope object at 0x41511bac>), ('ConsoleEchoer', <Repository.ClassScope object at 0x4115990c>)]
>>> (name,c)=cs[0]
>>> name
'ConsoleReader'
>>> c
<Repository.ClassScope object at 0x41511bac>
```

And look at properties of that component:

``` {.literal-block}
>>> c.module
'Kamaelia.Util.Console'
>>> c.inboxes
{'control': 'NOT USED', 'inbox': 'NOT USED'}
>>> c.outboxes
{'outbox': 'Lines that were typed at the console', 'signal': 'NOT USED'}
>>> print c.doc
ConsoleReader([prompt][,eol]) -> new ConsoleReader component.

Component that provides a console for typing in stuff. Each line is output
from the "outbox" outbox one at a time.

Keyword arguments:

- prompt  -- Command prompt (default=">>> ")
- eol     -- End of line character(s) to put on end of every line outputted (default is newline)
```

This includes methods defined in it:

``` {.literal-block}
>>> c.listAllFunctions()
[('main', <Repository.FunctionScope object at 0x4166822c>), ('__init__', <Repository.FunctionScope object at 0x4166224c>)]
>>> name,f=c.listAllFunctions()[1]
>>> name
'__init__'
>>> f
<Repository.FunctionScope object at 0x4166224c>
```

We can look at the docs for the function:

> ``` {.doctest-block}
> >>> f.doc
> 'x.__init__(...) initializes x; see x.__class__.__doc__ for signature'
> ```

We can ask for a string summarising the method\'s arguments:

``` {.literal-block}
>>> f.argString
'self[, prompt][, eol]'
```

Or a list naming each argument, consisting of (argname,
summary-representation) pairs:

``` {.literal-block}
>>> f.args
[('self', 'self'), ('prompt', '[prompt]'), ('eol', '[eol]')]
```
:::
:::

::: {.section}
[Obtaining introspection data]{#obtaining-introspection-data} {#46}
-------------------------------------------------------------

To get a detailed introspection you create a ModuleDoc object. You can
either point it at a specific directory, or just let it introspect the
currently installed Kamaelia repository.

You can specify the module path corresponding to that directory (the
\"root name\"). The default is simply \"Kamaelia\". If for example, you
point it at the
[Kamaelia.Chassis](/Components/pydoc/Kamaelia.Chassis.html){.reference}
directory; you should explain that the root name is
\"[Kamaelia.Chassis](/Components/pydoc/Kamaelia.Chassis.html){.reference}\".
Or if, for example, you are using this code to document
[Axon](/Docs/Axon/Axon.html){.reference}, you would specify a root name
of \"[Axon](/Docs/Axon/Axon.html){.reference}\".

After instantiating your ModuleDoc object; remember to call its
\"resolve\" method to allow it to resolve references to base classes,
and determine method the resolution order for classes.
:::

::: {.section}
[How are components and prefabs detected?]{#how-are-components-and-prefabs-detected} {#47}
------------------------------------------------------------------------------------

Components and prefabs are detected in sourcefiles by looking for
declarations of an \_\_kamaelia\_components\_\_ and
\_\_kamaelia\_prefabs\_\_ variables, for example:

``` {.literal-block}
__kamaelia_components__ = [ "IcecastClient", "IcecastDemux", "IcecastStreamWriter" ]
__kamaelia_prefabs__ = [ "IcecastStreamRemoveMetadata" ]
```

They should be declared individually, at module level, and should
consist of a simple list of strings giving the names of the
components/prefabs present.
:::

::: {.section}
[Structure of detailed introspections]{#structure-of-detailed-introspections} {#48}
-----------------------------------------------------------------------------

The introspection is a hierarchy of Scope objects, each representing a
delcaration scope - such as a module, class, function, etc. These are
built up to reflect the structure of the library if it is imported.

-   ModuleDoc objects represent each module. They may contain:

    > -   Other ModuleDoc objects
    > -   ImportScope objects
    > -   ClassScope objects (representing classes and components)
    > -   FunctionScope objects (repesenting functions and prefabs)
    > -   UnparsedScope objects (anything that wasn\'t parsed)

ClassScope and FunctionScope objects may also contain any of these. For
example, methods in a class will be represented as FunctionScope objects
within the ClassScope object.

The find() method of any given scope can be used to lookup a symbol in
that scope, or its children. For example, you could call find() on the
\"[Kamaelia.Chassis](/Components/pydoc/Kamaelia.Chassis.html){.reference}\"
ModuleDoc object with the argument \"Graphline.Graphline\" to retrieve
the graphline component (its full path is
\"[Kamaelia.Chassis.Graphline.Graphline](/Components/pydoc/Kamaelia.Chassis.Graphline.Graphline.html){.reference}\")

The listAllXXXXX() methods enumerate items - such as classes, functions,
components, prefabs or modules.
:::

::: {.section}
[Implementation Details]{#implementation-details} {#49}
-------------------------------------------------

This code uses the python compiler.ast module to parse the source of
python files, rather than import them. This allows introspection of code
that might not necessarily run on the system at hand - perhaps because
not all dependancies can be satisfied.

Basic tracking of assignment operations is performed, so the following
is fair game:

``` {.literal-block}
from Axon.Component import component as flurble

class Boo(flurble):
    pass

Foo=Boo
```

However anything more comple is not processed. For example, functions
and classes declared within \"if\" statement will not be found:

``` {.literal-block}
if 1:
    class WillNotBeDetected:
        pass

    def AlsoWillNotBeDetected():
        pass
```

The simplified functions that only return lists of component/prefab
names ( GetAllKamaeliaComponentsNested, GetAllKamaeliaComponents,
GetAllKamaeliaPrefabsNested and GetAllKamaeliaPrefabs) simply run the
full introspection of the codebase but then throw most of the
information away.
:::
:::

------------------------------------------------------------------------

::: {.section}
:::
:::

::: {.section}
Feedback
========

Got a problem with the documentation? Something unclear that could be
clearer? Want to help improve it? Constructive criticism is very welcome
- especially if you can suggest a better rewording!

Please leave you feedback
[here](../../../cgi-bin/blog/blog.cgi?rm=viewpost&nodeid=1142023701){.reference}
in reply to the documentation thread in the Kamaelia blog.
:::

*\-- Automatic documentation generator, 05 Jun 2009 at 03:01:38 UTC/GMT*
