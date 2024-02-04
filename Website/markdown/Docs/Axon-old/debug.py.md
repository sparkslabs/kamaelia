---
pagename: Docs/Axon-old/debug.py
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
[Axon.]{style="font-size:24pt"}[debug.py]{style="font-size:24pt;font-weight:600"}

Version: Axon 1.0.4

[What is it?]{style="font-weight:600"}

A simple debugging class.

[What is its purpose?]{style="font-weight:600"}

The purpose of this debug subsystem is to allow a configurable method
for debugging. When dealing with single threaded concurrency it can
become difficult to trace code, limiting the effectiveness of debuggers.
(Especially the kind that allows you to step through execution)

[How does it work?]{style="font-weight:600"}

The essential idea is this:

-   Sections of the code can be conceptually tagged with a name. This
    can be a function, a class, or an expected code flow.
-   Each tag has an associated debug level. A debug level of zero
    implies that debugging for that section is switched off. The higher
    the number, the greater the amount of debugging output.
-   Debugging statements can then be made with a tag & debug level -
    along with any arbitrary data represented as a string.

If one or more sections of code have an active tag, then a trace of what
they requested is output along with a small amount of data to assist
with debugging.

These sections, levels etc are defined in a \"debug.conf\" file in the
local directory. In the absence of a debug.conf file, the system uses
internal hard coded defaults.

One caveat: using a debug section/tag in code, but not defined in
defaults nor in a config file will crash. [This is by design.
]{style="font-style:italic"}The reason is simple - whilst developers may
wish to add random debug tags when creating their code, later when some
maintainer wishes to figure out what\'s broken, having a complete list
of all debug tags is vital. One way of ensuring this is to ensure
they\'re either in the defaults or in a supplied and always findable
debug.conf file. Quite how this will pan out in the long term is still
unclear, but the motivation will remain the same. (Implementation
approach may change of course!)

[debug.conf file format]{style="font-weight:600"}

The config file consists of a number of lines.

Each line is either a comment or config line

A comment line is either an empty line, or a line starting with a \'\#\'

A config line has 3 values:

section.tag debug.level debug.location

-   section.tag has the form \[a-zA-Z\]+(\\.\[a-zA-Z\]+)\* - ie a dotted
    alpha value.
-   debug.level is an integer, 0 or more
-   debug.location is currently just \"default\", but may change to gain
    extra values if appropriate at a later point in time.

eg:

[Sample trace output]{style="font-weight:600"}

[Sat Feb 26 08:26:39 2005 \| SimpleServerTestProtocol.mainBody \|
NetServ : We were sent data - ]{style="font-family:Courier 10 Pitch"}

[Sat Feb 26 08:26:39 2005 \| SimpleServerTestProtocol.mainBody \| We
should probably do something with it now?
:-)]{style="font-family:Courier 10 Pitch"}

[Sat Feb 26 08:26:39 2005 \| SimpleServerTestProtocol.mainBody \| I
know, let\'s sling it straight back at them
:-)]{style="font-family:Courier 10 Pitch"}

[Outstanding Issues]{style="font-weight:600"}

Just prior to the 1.0 release of Axon, we changed over to using setup.py
(ie distutils) for installation/packaging etc. Prior to this the code
expected to be run from a specific location and hence a debug.conf file
would always be available. This was disable prior to the actual 1.0
release, but it would be nice to re-enable the full system again.

There are a number of issues with the way debugging is handled at
present:

Configuration and defaults

-   Currently we allow a debug.conf file to override [all
    ]{style="font-style:italic"}values for debugging. What it should
    allow is allow the values for debugging to be replaced/merged - with
    the config values taking precedence.

Lack of decent test suite. (There is some partial testing, but it\'s
nowhere near complete)

Documentation for the debug API currently sucks. (The only real usage
docs would be to look at how Axon itself uses the debug subsystem)

Essentially the debugging divides the system into sections, and each
section can have a debug level. The higher the debug level, the more
output for that section you see. Debugging can also be switched on on a
[per component]{style="font-style:italic"} basis.

[Issues Resolved]{style="font-weight:600"}

-   Now have a set of defaults covering debugging. These will probably
    need to change as we need namespaces, but for now the defaults work.
    (Allowing debugging to really be available, reducing Heisenbug
    scenarios)
-   Previous speed related issues regarding debugging have been resolved
    (largely).

[Pydoc Style Documentation]{style="font-size:14pt;font-weight:600"}

class debug(object)

Methods defined here:

[\_\_init\_\_(self, assertBadDebug=1)]{style="font-weight:600"}

[debug(self, section, level, \*message)]{style="font-weight:600"}

-   Outputs \*message if user set level is greater than requested level
    for given section returns True. This allows debug to be used in
    assert statements to allow lazy evaluation of expressions in
    \*message so that they can disabled by running the system using
    python\'s -O flag

[note = debug(self, section, level, \*message)]{style="font-weight:600"}

-   note is an alias for debug.

[addDebug(self, \*\*debugSections)]{style="font-weight:600"}

[addDebugSection(self, section, level)]{style="font-weight:600"}

[decreaseDebug(self, section)]{style="font-weight:600"}

[increaseDebug(self, section)]{style="font-weight:600"}

[readConfig(self, configFile=\'debug.conf\')]{style="font-weight:600"}

[setDebugSections(self, \*\*debugSections)]{style="font-weight:600"}

[useConfig(self, filename=\'debug.conf\')]{style="font-weight:600"}

[Testdoc Documentation]{style="font-size:14pt;font-weight:600"}

[TODO: ]{style="font-weight:600"}Implement test suite for Axon.debug.py
(We did mention that tests were added late in the project?)

Michael, December 2004, February 2005
