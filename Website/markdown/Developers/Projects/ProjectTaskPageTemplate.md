---
pagename: Developers/Projects/ProjectTaskPageTemplate
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Project Task Page: Template
---------------------------

::: {.boxright}
**Status:** Started, Running, Completed, Dropped, Stasis, Blocked *-
Associated single sentence (eg why blocked)*\
**Current Developers:** *you!*\
**Current \"inflight\" dev location:** *Normally /Sketches/ initially*\
**Start Date:** *date*\
**Major Milestone date:** (met/slipped/missed) *(optional)*\
**Expected End Date:** *(n/a is valid, ASAP is not)*\
**End Date:** *date*\
**Date this page last updated:** *date*\
**Estimated effort so far:** *manday count*\
:::

***This page is a template. You are expected to replace the bulk of text
on this page with text relevant to your task, be it a bug fix, new
feature, new component, new system or new project. You may end up
deleting things. It is expected that the larger the task, the more
complete the page. For small tasks, especially those relating to a
single task as definite subtasks, you may simply describe them as
subtasks on the project task page for the parent project. (at minimum,
delete this text!)*\
**

**Description**
---------------

-   Short one line of what the task is designed to achieve/create.

```{=html}
<!-- -->
```
-   A practical, clear result of what will be possible as a result of
    achieving this task. This is best described in the case of a user
    story.\

```{=html}
<!-- -->
```
-   The context in which this task sits. Has this task any history? Is
    it the result of any previous tasks - either within the project or
    outside.

```{=html}
<!-- -->
```
-   What benefits will be gained by working on this task, and achieving
    its goals? Speculative as well as certained/realistically expected
    benefits are valid here.

Inputs
------

This section is largely about WHO has influenced this task to do WHAT,
and where possible WHY. It is also about WHO to contact with regard to
this task to influence what\'s going on.\

Task Sponsor: (can be main developer)

Task Owner: (likely to be main developer)\

Developers involved in the task at some point\

-   There is likely to be at least one. One will be the task owner (if
    the project is not in stasis)\

Users:

-   Specific concrete users who have provided input

Interested third parties

-   This will be specific third parties who have provided input to the
    project

Requirements

-   Each requirement should have who the requirement came from attached
    to it
-   Each requirement should have an indication of MUST/SHOULD/MAY/WOULD
    LIKE attached.

The people listed here should be real people. Unless you have agreement
however, this this should be their initials rather than name.\
\
Relevant Influencing factors:\

-   *eg release of a tool doing the same sort of thing that renders this
    non-relevant*
-   *people joining/leaving project*
-   *change of sponsorship*
-   *growth in users/thirdparties*
-   *tool dependency suitablility*
-   *unexpected complications*

Outputs
-------

This section is largely about WHAT has been produced, normally by WHO
(in order to provide a point of contact)\

### Expected

-   There is likely to be at least one thing expected\

### Actual

This can take many forms\

-   Code - what does it do, where is it?\
-   Reports - where is it, who wrote it, what was it about, when?\
-   Presentation - where is it, where was it presented, what was it
    about, who presented it, when?\
-   Events - eg The Brussels open space event
-   Other - other actual strands of work arising.\

Note: Especially with speculative tasks,actual outputs may be
substantially different from expected.\

### Realistic possibilities arising as a result of activity on this task

Generally speaking there may or may not be anything here. The reason
this is under outputs, is because this really is an output, even if it
doesn\'t look like it at first glance.\

Related Tasks
-------------

### Tasks that directly enable this task (dependencies) 

-   example: Multicast transciever, internet subsystem
-   This tasks should ideally be links to the project task pages for
    these other tasks.\

### Sub Tasks

-   Example: Selector subsystem shutdown
-   Each subtask here should ideally be a link to a project task page
    for that project
-   It would be *nice* but not mandatory to note the subtask status
-   For small subtasks, it **IS** acceptable to merely have subtasks as
    bullet points with the sort of information you\'d put on a project
    task page, but for which it seems overkill to create a project task
    page for. (It can always become a full PTP later on)\

Task Log
--------

*This is a list of time indexed day to day item. There should ideally be
an entry here every time you work on this task. Ideally the time taken
relating to each entry should be listed as well, preferably in man days,
down to 1/4 day granuarity. (ie 2 hours). Sanity is expected to prevail
when noting this down. They should be annotated by who made the entry,
when, and any status changes.*\

***When a task is running, then this is where most updates will
occur.**\
\
Please put **Output** in bold prior to any entries where an output was
produced\
Please put **Task status changed** in bold when the entry relates to a
task status change.\
Example entries:*\

-   Created the PTP page for the project, and brainstormed how to get
    started. Michael. November 27th 2006. Time spent 1/4 day
-   **Output:** Produced report (added to output list), Michael.
    November 27th 2006. Time spent 1/4 day.
-   Liased with sponsor (input to task). Michael, Sponsor, November
    27th 2006. Time spent 1/2 day.
-   Started working of frobbing the bibble, code is being worked in in
    /Sketches/MPS/Here/\...\
    **Task status changed** to running.\
    Time spent: 1/2 day\
    Michael, November 27th 2006\
-   Project blocked due to lack of access to kit, Michael, 27th
    November 2006. Time spent: n/a, **Task status changed** to blocked.
-   Changed sponsor to Jimbo
-   Added developer Matt
-   Removed developer Michael
-   Removed developer Matt
-   **Task status changed** to stasis

This is however a task log. The format of entries hasn\'t be decided on
yet. However there should ideally be an entry an minimum whenever the
state of the task changes - that is new developers, sponsors, inputs
from people, outputs from the task, whether the project is completed,
finished etc.\
The reason for including times is to assist in future time estimation
exercises.\
As a result each entry is likely to have:\

-   A note of any state change (new person, new input, new output,
    status change, new work started, completed etc) This can however
    simply be a note to say what\'s been done in that amount of time
    working on the task. eg code refactoring is none of the above, but
    is work, and is suitable for the task log, as is simply \"coding,
    Michael, November 27th, 1 day\", etc
-   Who is making the entry
-   When they are making the entry
-   The amount of time spent in the process of effecting that entry. (eg
    1/2 day writing a report, 1/2 writing code, etc)

I\'d expect much of this text to be deleted.\
\

Discussion
----------

This is where random comments with regard to the project can be added.
It\'s expected this section will be in thread mode rather than document
mode, but people should feel able to refactor comments. If they do,
these comments become inputs to the project, and the people who have
added comments would be added under interested third parties.

Anything that doesn\'t fit above fits in here.

#### end note (delete from any actual PTP)

This is an idea of how to capture project tasks, their dependencies,
etc. It\'s not expected to be followed slavishly but with common sense.
If it seems dumb, try changing things, and see how it works out.
Preferably with discussion!\

\-- Michael Sparks, November 27th 2006

\
