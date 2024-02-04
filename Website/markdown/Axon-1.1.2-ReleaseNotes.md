---
pagename: Axon-1.1.2-ReleaseNotes
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
[Axon Release Notes]{style="font-size:24pt;font-weight:600"}

[1.1.2]{style="font-size:18pt"}

[Summary]{style="font-size:18pt;font-weight:600"}

Instated use of ctypes to use posix.sched\_yield during the main loop.
This makes the system a \*little\* bit more other-system friendly.

Added in the ability to do, effectively, blocking calls to other
components. The best example using this at present in
Kamaelia.UI.Pygame.Ticker

Specifically you can ask the system to run a different microprocess in
the place of the running one, and wait until it ends.

Where self.requestDisplay is a generator with the following behaviour:

This is experimental support that is likely to evolve with time. This
does however allow effectively for a far more co-routine type behaviour
than we had in place before - rather than generator type behaviour.

[Detailed Changelog]{style="font-size:18pt;font-weight:600"}

[Changed Files:]{style="font-size:14pt"}

Axon.Component.component:

-   Added introspectable documentation to the purposes of the default
    inboxes and outboxes. component.Inboxes\[\"inbox\"\] gives you
    documentation on that inbox

Axon.Ipc.py:

-   WaitComplete\
    New IPC class allowing components to signal to the scheduler that
    they\'d like a generator started, run to completion and then control
    handed back to the original generator. This is similar, in a way, to
    call with continuation or similar to nesting yields in a system like
    greenlets, but having the stacking of frames essentially handled by
    main system.\
    \
    This is experimental support initially. This will probably become
    more generalised with time, but for the moment it\'s put in place to
    cover a specific use case - getting a pygame display. This is likely
    to be useful in a variety of locations however.\
-   reactivate is a sister IPC function to reactivate the original
    generator (ie main()) when the call is finished.

Axon/Microprocess.py:

-   microprocess class constructor extended to allow a generator object
    to be be passed in as the \_\_thread of control for the
    microprocess. This is to support the WaitComplete functionality.
    This means arbitrary generators can be embdedded into a microprocess
    and scheduled, without creating a new class for the generator. (This
    has scope for use outside the core of Kamaelia of course).\
    \
    It has also been extended to allow the addition of a closeDownValue.
    This is a value the scheduler can look at when the microprocess
    finishes and can decide what to do next. An example would be to
    reactivate a previous thread of control using the new \'IPC\'
    message \"reactivate\".

Axon/Scheduler.py:

-   A number of changes. The bulk of code change relates to code
    deletion. Specifically the deletion of debugging code that has not
    been need in over a year now. Clearly this could be re-instated
    easily in a targetted fashion, but for now is not needed.
-   The addition of code supporting the new experimental WaitComplete
    functionality. (Experimental in terms of \"what can it do\", not in
    terms of \"does it work\" - it works.)
-   The instatement of the use of ctypes (conditional import) to allow
    the scheduler to periodically make a posix.sched\_yield call.
-   Change to add in a method for handleMicroprocessShutdownKnockon to
    handle shutdown of items postmen, and WaitComplete objects.
-   self.time added - which means a generator can now find out system
    time by querying self.scheduler.time. It isn\'t clear if this is a
    good or bad idea as yet.
