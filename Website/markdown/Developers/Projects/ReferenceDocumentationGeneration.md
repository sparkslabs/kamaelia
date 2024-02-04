---
pagename: Developers/Projects/ReferenceDocumentationGeneration
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Project Task Page: Reference Documentation automated Generation 
---------------------------------------------------------------

::: {.boxright}
**Status:** Completed\
**Current Developers:** MH, MPS\
**Current \"inflight\" dev location:**
/Code/Python/Kamaelia/Tools/DocGen\
**Start Date:** *09 March 2006*\
**Major Milestone date:** April 2007 - Auto generation of Axon &
Kamaelia docs (met)\
**End Date:** 5 Aug 2007\
**Date this page last updated:** 5 Aug 2007\
**Estimated effort so far:** 30\
:::

**\
**

**Description**
---------------

-   Write a software tool(s) to generate HTML reference documentation
    for the Kamaelia component repository, and for Axon.
-   Arrange for automatic refreshing of the reference documentation on
    the website

\
Up-to-date automatically generated reference documentation is useful to
users/developers. If it is automatically rebuilt and uploaded to the
kamaelia website regularly then it is one less maintenance task.\

Inputs
------

Task Sponsor: MS

Task Owner: MH\

Developers: MS, MH

Users: MS, MH

Interested third parties: \--\

Requirements

-   MUST: Generate HTML output suitable for inclusion on the Kamaelia
    website\
-   MUST: Document components and prefabs in Kamaelia
-   MUST: Document classes and functions in Axon\
-   SHOULD: Include test suite results
-   SHOULD: Not have to import python modules to document them\
-   WOULD-LIKE: for regular (nightly?) automated rebuilds of docs and
    uploads to the Kamaelia website\

The people listed here should be real people. Unless you have agreement
however, this this should be their initials rather than name.\
\
Relevant Influencing factors:\

-   *feedback from people on \#kamaelia irc channel*
-   *lack of detailed introspection by existing
    Kamaelia.Support.Data.Repository code (not designed for that
    purpose)\
    *

Outputs
-------

### Expected

-   Documentation generation tool\

### Actual

Code:

Documentation generation tool:\

-   /Code/Python/Kamaelia/Tools/DocGen/DocExtractor.py
-   /Code/Python/Kamaelia/Tools/DocGen/renderHTML.py
-   /Code/Python/Kamaelia/Tools/DocGen/Node.py

Test Suite output generation tool:\

-   /Code/Python/Kamaelia/Tools/DocGen/TestSuiteRun.py

More detailed repository/codebase introspection

-   /Code/Python/Kamaelia/Kamaelia/Support/Data/Repository.py

Automation scripts on bbc.kamaelia.org for nightly rebuilds of docs

-   also checked into /Sketches/MH/AutoDocBuilding/

Nightly rebuilds of Axon and Kamaelia reference documentation now
automated.

Improvements to \"Compose\" tool:

-   /Code/Python/Kamaelia/Tools/Compose/GUI/ArgumentsPanel.py
-   /Code/Python/Kamaelia/Tools/Compose.py\

\
\

### Realistic possibilities arising as a result of activity on this task

\--\

Related Tasks
-------------

### Tasks that directly enable this task (dependencies) 

-   \--\

### Sub Tasks

-   Improved repository scanning (to detect components, prefabs, etc..
    and collect documentation etc)\
-   Setting up automatic rebuilding of docs on the website using the
    tools developed here\

Task Log
--------

-   09 March 2006 : **Task status changed** to running\
-   09 March 2006 : Added developer: Michael
-   09 March 2006 : Development commenced in
    /Sketches/MPS/DocExtractor.py\
-   12 March 2006 : First version of code complete. Kamaelia component
    docs built and uploaded manually to website manually.
-   15 March 2006 : **Task status changed** to stasis
-   \...\
-   26 February 2007 : Added developer Matt
-   26 February 2007 : **Task status changed** to running
-   26 February 2007 : Development re-commenced in /Sketches/MH/DocGen/
-   08 April 2007 : New code complete. Automated nightly rebuilds and
    uploaded set up on bbc.kamaelia.org
-   11 April 2007 : MH : Code moved from /Sketches/MH/DocGen/ to
    /Code/Python/Kamaelia/Tools/\
-   11 April 2007 : MH : Created this PTP
-   11 April 2007 : MS : **Tasks status changed** to stasis
-   \...\
-   23 May 2007 : MH : **Task status changed** to running
-   23 May 2007 : MH : Development re-commenced in
    /Sketches/MH/DocGen/ - aim to add documenting of inherited methods
-   23 May 2007 : MH : Experimenting with rewriting AST parsing code to
    track imports, assignments, etc.
-   18 June 2007 : MH : Created branch
    /private\_MH\_20070618\_docgen\_improvements/
-   18 June 2007 : MH : Adapted Compose.py (in branch) to use repository
    code instead of importing all the components
-   19 June 2007 : MH : Branch ready for merge (see below)
-   1 Aug 2007: MPS : Merged, has knock on for new bugfixes based on
    this changeset.\

Discussion
----------

\
Documentation generation is capable of building reference documentation
both: for Kamaelia components and prefabs; and also for Axon classes and
functions\
\
Part of this work included a ground-up rewrite of
Kamaelia.Support.Data.Repository to:\

-   scan a code base by parsing the source files rather than importing
    them (so docs can be rebuilt on a machine that doesnt have all
    kamaelia dependencies installed)
-   extract substantially more information - not just component names,
    but full doc strings, methods, inboxes, outboxes, method arguments
    etc. also also to extract prefabs, classes, functions and module
    level docs too\

\
**Running systems:**\

-   A nightly cron-job is now running on bbc.kamaelia.org that rebuilds
    both Axon and Kamaelia documentation and uploads it to the website.
-   If the cron-job fails, then kamaelia-commits is emailed to notify
    developers of the failure.\

\-- Matt, 11 April 2007\

**Branch private\_MH\_20070618\_docgen\_improvements (ready for merge)**

The repository introspection code has been rewritten so it now parses
source files using a process more akin to execution - it tracks imports,
class and function declarations, and assignment statements as it parses
the code. This means that, for example, it will no longer be fooled by
something like this:

>     from Axon.Component import component as C
>
>     class MyComponent(C):
>         ....
>
>     MyActualComponent = MyComponent
>     MyComponent = None

This new code will correctly determine that MyActualComponent inherits
from Axon.Component.component and that MyComponent doesn\'t actually
reference a component once the module is imported.\
\
This has therefore made it possible to determine what methods are
inherited from base classes. The documentation generator can therefore
provide more comprehensive class documentation for Axon. Mappings of
symbols to URLs can also be exported from a documentation build to a
file; and then re-imported for another build - thereby making it
possible to cross-link from Kamaelia component docs back to Axon docs.\
\
The nightly documentation build automation scripts (held in
/Sketches/MH/AutoDocGeneration) have been updated to use these new
capabilities, but this has not yet been uploaded to bbc.kamaelia.org\
\
Finally, the \"Compose\" tool has also been modified so it no longer
imports components - but instead uses the introspection data that comes
from this repository scanning code.\

\-- Matt, 19 June 2007\
