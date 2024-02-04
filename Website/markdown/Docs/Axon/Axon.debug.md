---
pagename: Docs/Axon/Axon.debug
last-modified-date: 2009-12-09
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
::: {.container}
::: {.section}
::: {.section}
[Axon](/Docs/Axon/Axon.html){.reference}.[debug](/Docs/Axon/Axon.debug.html){.reference}
----------------------------------------------------------------------------------------
:::
:::

::: {.section}
Internal debugging support - debug output logging
=================================================

::: {.container}
-   **class [debug](/Docs/Axon/Axon.debug.debug.html){.reference}**
:::

-   [How to use it](#83){.reference}
-   [Adjusting the configuration of individual debugger
    objects](#84){.reference}
:::

::: {.section}
Provides a way to generate debugging (logging) output on standard output
that can be filtered to just what is needed at the time.

-   Some Axon classes create/use write debug output using an instance of
    debug()
-   debug uses debugConfigFile.readConfig() to read a configuration for
    what should and should not be output

What debugging output actually gets output (and what is filtered out) is
controlled by two things: what *section* the debugging output is under
and the *level* of detail of a given piece of output.

Each call to output debugging information specifies what section it
belongs to and the level of detail it represents.

The filtering of this is configured from a configuration file (see
Axon.deugConfigFile for information on the format) which lists each
expected section and the maximum level of detail that will be output for
that section.

::: {.section}
[How to use it]{#how-to-use-it} {#83}
-------------------------------

Create a debug object:

``` {.literal-block}
debugger = Axon.debug.debug()
```

Specify the configuration to use, either specifying a file, or letting
the debugger choose its own defaults:

``` {.literal-block}
debugger.useConfig(filename="my_debug_config_file")
```

Any subsequent debug objects you create will use the same configuration
when you call their useConfig() method - irrespective of whether you
specify a filename or not!

Call the note() method whenever you potentially want debugging output;
specifying the \"section name\" and minimum debug level under which it
should be reported:

``` {.literal-block}
while 1:
    ...
    assert self.debugger.note("MyObject.main", 10, "loop begins")
    ...
    if something_happened():
        ...
        assert self.debugger.note("MyObject.main", 5, "received ", msg)
        ...
```

-   Using different section names for different parts of your debugging
    output allow you to select which bits you are interested in.
-   Use the \'level\' number to indicate the level of detail of any
    given piece of debugging output.

The note() method always returns True, meaning you can wrap it in an
assert statement. If you then use python\'s \"-O\" command line flag,
assert statements will be ignored, completely removing any performance
overhead the due to the debugging output.
:::

::: {.section}
[Adjusting the configuration of individual debugger objects]{#adjusting-the-configuration-of-individual-debugger-objects} {#84}
-------------------------------------------------------------------------------------------------------------------------

All debug objects share the same initial configuration - when you call
their useConfig() method, all pick up the same configuration file that
was specified on the first call.

However, after the useConfig() call you can customise the configuration
of individual debug objects.

You can increase or decrease the maximum level of detail that will be
output for a given section:

``` {.literal-block}
debugger.increaseDebug("MyObject.main")
debugger.decreaseDebug("MyObject.main")
```

You can add (or replace) the configuration for individual debugging
sections - ie. (re)specify what the maximum level of detail will be for
a given section:

``` {.literal-block}
debugger.addDebugSections()
```

Or you can replace the entire set:

``` {.literal-block}
replacementSections = { "MyObject.main" : 10,
                        "MyObject.init" : 5,
                        ...
                      }

debugger.addDebug(**replacementSections)
```
:::
:::

------------------------------------------------------------------------

::: {.section}
[Axon](/Docs/Axon/Axon.html){.reference}.[debug](/Docs/Axon/Axon.debug.html){.reference}.[debug](/Docs/Axon/Axon.debug.debug.html){.reference}
==============================================================================================================================================

::: {.section}
class debug(object) {#symbol-debug}
-------------------

::: {.section}
debug(\[assertBadDebug\]) -\> new debug object.

Object for outputting debugging output, filtered as required. Only
outputs debugging data for section names it recognises - as specified in
a debug config file.

Keyword arguments:

-   assertBadDebug \-- Optional. If evaluates to true, then any debug
    output for an unrecognised section (as defined in the configuration)
    causes an exception (default=1)
:::

::: {.section}
### Methods defined here

::: {.section}
#### [\_\_init\_\_(self\[, assertBadDebug\])]{#symbol-debug.__init__}
:::

::: {.section}
#### [addDebug(self, \*\*debugSections)]{#symbol-debug.addDebug}

Add several debug sections. Each argument\'s name corresponds to a
section name fo rwhich debug output can be generated. The value is the
maximum debug level for which there will be output.

This does not affect the configuration of other debug objects.
:::

::: {.section}
#### [addDebugSection(self, section, level)]{#symbol-debug.addDebugSection}

Add a section name for which debug output can be generated, specifying a
maximum debug level for which there will be output.

This does not affect the configuration of other debug objects.
:::

::: {.section}
#### [areDebugging(self, section, level)]{#symbol-debug.areDebugging}

Returns true if we are debugging this level, doesn\'t try to enforce
correctness
:::

::: {.section}
#### [debug(self, section, level, \*message)]{#symbol-debug.debug}

Output a debug message.

Specify the \'section\' the debug message should come under. The user
will have specified the maximum \'level\' to be outputted for that
section.

-   Use higher level numbers for more detailed debugging output.
-   Use different section names for different parts of your code to
    allow the user to select which sections they want output for

Always returns True, so can be used as argument to an assert statement.
This means you can then disable debugging output (and any associated
performance overhead) by using python\'s \"-O\" command line flag.

Keyword arguments:

-   section \-- the section you want this debugging output classified
    under
-   level \-- the level of detail of this debugging output (number)
-   \*message \-- object(s) to print as the debugging output
:::

::: {.section}
#### [debugmessage(self, section, \*message)]{#symbol-debug.debugmessage}

Output a debug messge (never filtered)

Keyword arguments:

-   section \--
-   \*message \-- object(s) to print as the debugging output
:::

::: {.section}
#### [decreaseDebug(self, section)]{#symbol-debug.decreaseDebug}

Decreases the maximum debug level for which output will be generated for
the specified section.

This does not affect the configuration of other debug objects.
:::

::: {.section}
#### [increaseDebug(self, section)]{#symbol-debug.increaseDebug}

Increases the maximum debug level for which output will be generated for
the specified section.

This does not affect the configuration of other debug objects.
:::

::: {.section}
#### [note(self, section, level, \*message)]{#symbol-debug.note}

Output a debug message.

Specify the \'section\' the debug message should come under. The user
will have specified the maximum \'level\' to be outputted for that
section.

-   Use higher level numbers for more detailed debugging output.
-   Use different section names for different parts of your code to
    allow the user to select which sections they want output for

Always returns True, so can be used as argument to an assert statement.
This means you can then disable debugging output (and any associated
performance overhead) by using python\'s \"-O\" command line flag.

Keyword arguments:

-   section \-- the section you want this debugging output classified
    under
-   level \-- the level of detail of this debugging output (number)
-   \*message \-- object(s) to print as the debugging output
:::

::: {.section}
#### [readConfig(self\[, configFile\])]{#symbol-debug.readConfig}

**INTERNAL** Reads specified debug configuration file.

Uses
[Axon.debugConfigFile](/Docs/Axon/Axon.debugConfigFile.html){.reference}
:::

::: {.section}
#### [setDebugSections(self, \*\*debugSections)]{#symbol-debug.setDebugSections}

Set the debug sections. Replaces any existing ones.

Each argument\'s name corresponds to a section name fo rwhich debug
output can be generated. The value is the maximum debug level for which
there will be output.

> This does not affect the configuration of other debug objects.
:::

::: {.section}
#### [useConfig(self\[, filename\])]{#symbol-debug.useConfig}

Instruct this object to set up its debugging configuration.

If this, or another debug object has previously set it up, then that is
applied for this object; otherwise it is loaded from the specified file.
However, if no file is specified or the file could not be read, then
alternative defaults are used. This configuration is then used for all
future debug objects.
:::
:::

::: {.section}
:::
:::
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

*\-- Automatic documentation generator, 09 Dec 2009 at 04:00:25 UTC/GMT*
