---
pagename: Axon-1.5.0-ReleaseNotes
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
[Axon Release Notes]{style="font-size:28pt;font-weight:600"}

[1.5]{style="font-size:21pt"}

[Summary]{style="font-size:21pt;font-weight:600"}

Axon 1.5 is a major performance related release for Kamaelia\'s core
component system. There have been a number of core changes, some
highlights:

Zero copy delivery of data from producers to consumers

The system scheduler is now reactive to threaded components, meaning the
system can truly sleep when there is nothing to do.

This means self.pause() REALLY pauses the microprocess, and may result
in the component not receiving data. (If you call self.pause, you should
really mean it). Generally this is only used at an optimisation stage.

Threaded components are now fully supported with the following caveats:

-   They should not use the shared environment provided the
    co-ordinating assistant tracker (they\'re not expected to need to do
    so, but this is useful to make explicit)
-   They should not expect to be able to interact with synchronous boxes
    (boxes with a maximum size)

<div>

Aside from these caveats, creating and using a threaded component is the
same as a normal generator based one, except you simply don\'t have
yield statements. You obviously use a different base class.

</div>

The use of the \"ipc\" message Axon.Ipc.newComponent for child component
startup has been deprecated in favour of the simpler API:

Despite all these changes, components written for earlier versions of
Axon will continue to work as before.

Documentation has also generally improved,and is included in the the
code files for access via pydoc/help.

[Changelog]{style="font-size:21pt;font-weight:600"}

Major subsystem changes aimed at performance enhancements

[Message Passing and Delivery Optimisation
Changes]{style="font-weight:600"}

-   Boxes are now discrete objects. This change has occured to enable
    the use of direct (effectively \"zero copy\" delivery).
-   This has meant the postman has been deleted - components no longer
    have a postman associated with them. This also dramatically frees up
    CPU cycles for components rather than the communications system.
-   To replace the structural tracking, a \"postoffice\" class has been
    created instead. This, however, is passive rather than active.
-   Because the death of a component no longer also means the death of a
    postman, microprocess has been simplified to remove the concept of
    activity creator. This removes the knock on complexity in both the
    scheduler and inside Component.
-   Despite these changes components running on top of Axon (ie existing
    Kamaelia components) operate largely unchanged. (A few that assumed
    the existance of a postman etc have changed)

[Flow Control Inversion]{style="font-weight:600"}

-   The Scheduler therefore now dynamically builds its runqueue to only
    include unpaused (active) microprocesses.
-   If there are no active microprocesses, the scheduler can now sleep.
    Reducing CPU usage to zero, until some kind of event causes
    something to wake up. Flow of control is therefore effectively
    inverted as Axon systems can now be reactive.
-   Pausing state is now managed by the scheduler on behalf of
    microprocesses (they used to manage it themselves). Requests to wake
    and pause microprocesses get routed to the Scheduler.
-   The APIs for Component and Microprocess are, for the most part,
    unchanged. Existing components will continue to work as before. If
    they self pause they will benefit from reduced CPU usage. If all
    components in a system behave in this way, then Axon will cease to
    busy-wait when idle.

[Threading Support]{style="font-weight:600"}

-   The threaded component has had its API fixed to match the rest of
    Axon (with the obvious exception of removing the yields).
-   Threaded \'adaptive\' component is new.

[Other]{style="font-weight:600"}

-   Bug fix to make Wait\* work cleaner

Axon.Component.Component

-   Default documentation for Component class in/out- boxes added
-   anyReady() added. Returns true if any has data in it.

Axon.Microprocess.Microprocess

-   Can activate an arbitrary thread of control from a generator (The
    thing you normally call .next() on)
-   Can pass on a closeDownValue
-   Can be set as an activity creator
-   Now conditionally starts the thread. Actually helps with re-entrant
    calls inside a single active microprocess.

Axon.Scheduler.Scheduler

-   Now handles shutdown knockons more gracefully
-   Removal of lots of debugging code no longer needed (hasn\'t been
    needed in a long while)
-   Code cleanup

Axon.Ipc

-   Added the shutdown message. This can be used to request that an Axon
    component should simply shutdown. This does not force the component
    to shutdown, merely requests it.

[Synchronous Links & Link Tracing API]{style="font-weight:600"}

As part of the changes to box optimisations, there has been a change to
the API for synchronous links. This is currently our best guess as to
what we think makes sense, but should be considered experimental until
Axon 2.0 (We\'ll endevour to keep the current API however for as long as
it makes sense).

When a synchronous link reaches maximum capacity, attempting to send
data to the synchronous link results in an exception being thrown. This
includes the current size of the pipe, and it\'s maximum capacity. The
exception thrown is as follows:

[Detailed Changes to files]{style="font-size:21pt;font-weight:600"}

Changes to Component class:

-   Number of changes to support the newstyle boxes. (send now results
    in direct delivery)
-   \_collect method removed.
-   \_deliver method deprecated (except for tests and debugging)
-   anyReady method added to check to see if any inbox has data ready.
-   Implementation detail of \_activity creator removed \-- no longer
    needed.
-   Removal of synchronisedSend method.

Misc:

-   An arbitrary generator can now be scheduled (using a wrapped call).
-   Subclasses of microprocesses can now have a different named \"main\"
    method.
-   Axon/\_\_init\_\_.py - added ThreadedComponent module initialisation

Adaptive inboxes changed into a mixin class:

-   Reused in both Axon/AdaptiveCommsComponent.py and
    Axon/ThreadedComponent.py
-   to provide adaptive inboxes for both generator based and thread
    based components.

New Axon/Ipc.py Messages:

-   ipc
-   reactivate FIXME: is this used now?
-   WaitComplete FIXME: example of usage.

Changes to allow scheduling to be reactive to threaded components:

-   Axon/Scheduler.py
-   Axon/Microprocess.py

Largely Rewritten or initial release:

-   Axon/ThreadedComponent.py (cleanup of external API and
    implementation)
-   Axon/Linkage.py (due to changes to message delivery, much
    simplified)
-   Axon/Box.py
-   Axon/Postoffice.py

Improved documentation:

-   Axon/AdaptiveCommsComponent.py
-   Axon/Component.py
-   Axon/Ipc.py
-   Axon/Linkage.py
-   Axon/ThreadedComponent.py
-   Axon/Scheduler.py

Test suite moved out into separate tree. (being inside the installation
area doesn\'t seem to make sense)

-   Axon/test/test\_util.py
-   Axon/test/test\_idGen.py
-   Axon/test/test\_debugConfigFile.py
-   Axon/test/test\_debug.py
-   Axon/test/test\_\_\_str\_\_.py
-   Axon/test/test\_Scheduler.py
-   Axon/test/test\_Microprocess.py
-   Axon/test/test\_Linkage.py
-   Axon/test/test\_Ipc.py
-   Axon/test/test\_CoordinatingAssistantTracker.py
-   Axon/test/test\_Component.py
-   Axon/test/test\_Axon.py
-   Axon/test/test\_AdaptiveCommsComponent.py
-   Axon/test/debug.conf
-   Axon/test/TemplateTestModule.py
-   Axon/test/AxonTest.py

Obsolete, due to box optimisations:

-   Axon/test/test\_Postman.py
-   Axon/Postman.py

Changed due to removal of the Postman:

-   Axon/\_\_init\_\_.py (import postoffice instead of postman)
-   Axon/Component.py

Michael, June 2006
