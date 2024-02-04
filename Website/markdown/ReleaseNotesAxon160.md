---
pagename: ReleaseNotesAxon160
last-modified-date: 2008-10-19
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Axon Release Notes: 1.6.0
=========================

New Files & Functionality 
-------------------------

    Index: Axon/Handle.py

    Rewritten replacement for LikeFile. Intended to be used with
    Axon.background. Handle and code using it is experimental at
    present. See Examples/Handle for how to use this.

    Handle is specifically designed to allow you to use Kamaelia components
    and subsystem in non-kamaelia systems. It does this by providing you
    with a "Axon.Handle" which is conceptually similar to a "file handle".
    The interface allows you to start components in the background, and
    read from it's outboxes, and write to it's inboxes in a non-blocking
    fashion.

    The fact that it's non-blocking does mean that exceptions can be thrown
    if the component isn't ready for some reason, but this is intentionally
    similar to talking a non-blocking file handle.

    Note: whilst Handle is conceptually similar to a file handle, since you
    have multiple data sources and data sinks inside a component, the interface
    is not the same as the file interface since it wouldn't be appropriate.
    However, given the usage style is similar, that's why the name of this
    facility is "Handle".

    Limitations:
     * It currently will only allow access to components with the
       default/standard inboxes of inbox/control/signal/outbox.
     * This is a known limitation, but covers a wide class of situations.

    Please look at the examples for details.

    Index: Axon/background.py
        * This provides facilities for running the Axon scheduler in a
          background thread. This is useful for integrating Kamaelia code
          with non-Kamaelia based systems - especially those that MUST own
          the primary thread (eg various windowing systems).
        * Expected to be used with Axon.background.
        * Please see Examples/Handle for examples of usage.
        * Simplest usage:
              from Axon.background import background
              from Kamaelia.UI.Pygame.MagnaDoodle import MagnaDoodle
              import time

              background = background().start()

              MagnaDoodle().activate()
              while 1:
                  time.sleep(1)
                  print "."

    Index: Axon/STM.py
       * Support for basic in-process software transactional memory.

       * Software Transactional Memory (STM) is a technique for allowing
         multiple threads to share data in such a way that they know when
         something has gone wrong. It's been used in databases (just called
         transactions there really) for some time and is also very similar
         to version control. Indeed, you can think of STM as being like
         variable level version control. (If you ignore history and are
         just after version numbers(!))

       * This is provided for those times when you really DO need to share
         values between threads/component.

    Index: Axon/experimental/_pprocess_support.py
       * The internals of this are strictly private from an API perspective.
         It's actually based on an older version of Axon.Handle which works
         sufficiently well for Axon.experiment.Process, but not for general
         support. (essentially it's the old Axon.LikeFile code, which was
         experimented with between Axon 1.5 and 1.6)

    Index: Axon/experimental/Process.py
       * Provides the core for multiprocess support in Kamaelia.
         Specifically provides ProcessPipeline and ProcessGraphline. At
         present thse are limited in the inboxes/outboxes you can use for
         linkages to just inbox/outbox/control/signal. This is a
         limitation, but sufficient in many contexts.

    Index: Examples/STM/Philosophers.py
       * An example of how to implement dining philosophers with pure
         python threads and Axon's STM code.

    Index: Examples/STM/Axon.Philosophers.py
       * An example of how to implement dining philosophers with
         Axon ThreadedComponents and Axon's STM code.

    Index: Examples/SystemShutdown.py
        * Example of how to use the new self.scheduler.stop() facility in
          Axon, both in terms of shutting down the system and also in terms
          of shutting down components that don't actually support shutting
          down directly.

    Index: Examples/Handles/TestHandle.py
        * An acceptance test for using Axon.Handle to act as a manual
          intermediary between 2 Kamaelia components in a non-Kamaelia
          system.

          Ie read from this one, pass onto that one - core of the code for
          that is this:
               while 1:
                   time.sleep(1)
                   try:
                      data = TB.get("outbox")
                      print data
                      message = data
                   except Queue.Empty:
                      pass
                   TD.put(message, "inbox")

    Index: Examples/Handles/reverser.py
       * And example of how to use Handle with a trivial component that
         reverses lines of data passed to it. (The aim is not to demo the
         component, but how to use the component in a non-Kamaelia system)
         After all, the component could be accessing a remote web service
         instead.

Axon Files Changed and Changes in this release 
----------------------------------------------

    Index: Axon/Component.py
        * Copyright notice change
        * Documentation changed to REST format
        * Extensive Documentation improvements
        * change to support this:
        * +      self.__dict__.update(argd)
           -- Major change/improvement despite appearances
        * Components can now be awoken when a component
          *leaves* an outbox again.
        * New method:
               def setInboxSize(self, boxname, size):
                    "boxname - some boxname, must be an inbox ;
                     size - maximum number of items we're happy
                     with"
        * Extra debugging assistance in some unusual situations,
          specifically designed to catch where someone uses the
          class where they should be using an instance when
          creating sub components.
        * New method:
        +   def Inbox(self, boxname="inbox"):
        +       while self.dataReady(boxname):
        +           yield self.recv(boxname)

    Index: Axon/Box.py
       * Copyright notice
       * Module documentation added - REST format
         * nullsink Class documentation added
            * Method documentation added
         * realsink Class documentation added
            * Method documentation added

         * postbox Class documentation clarified
            * Init gains notify method
            * Ahhh, "wake on object taken from outbox implemented",
              this is implemented using notify and following down
              the chain of linkages.
            * Notify on pop added
               * Variety of knockons in lots of places.
               - Cause of many of the changes to this module.
            * Method documentation added

    Index: Axon/Introspector.py
        * Documentation changed to REST format
        * Documentation improvements
        * Added documentation of internals

    Index: Axon/__init__.py
        * Documentation changed to REST format
        * Documentation added, matching new autodocs system
        * Code tidying

    Index: Axon/Postoffice.py
        * Documentation changed to REST format
        * Major documentation improvements.
        * Adds in BoxAlreadyLinkedToDestination error
           - thrown if the user tries to link an outbox to a
             destination, when it is already linked to a
             destination.

    Index: Axon/ThreadedComponent.py
        * Documentation changed to REST format
        * Major documentation improvements.
        * Minor bugfix ( _threadrunning flag)
        * stuffWaiting = True commented out
        * Fixes regarding waking a thread back up when a message is
          taken from it's outbox. (ie improvements to unpausing
          when message taken from outbox)
          (hence removal of stuffWaiting flag)
        * Unpauses on recv from inbox.
        * Unpauses on send to outbox
        * Minor changes to improve responsiveness when pausing

    Index: Axon/debugConfigDefaults.py
        * Documentation changed to REST format
        * Major documentation improvements.

    Index: Axon/Axon.py
        * Documentation changed to REST format
        * Removed the metaclass created __super() method
          convenience function - it's been deprecated for
          a long time since there's boundary issues where
          it would go wrong.

    Index: Axon/AxonExceptions.py
        * Documentation changed to REST format
        * Major documentation improvements.
        * New exception: BoxAlreadyLinkedToDestination
          The inbox/outbox already has a linkage going *from* it
          to a destination.

          Possible causes:
              - Are you trying to make a linkage going from an
                inbox/outbox to more than one destination?
              - perhaps another component has already made a
                linkage from that inbox/outbox?

    Index: Axon/Microprocess.py
        * Documentation changed to REST format
        * Major documentation improvements.
        * Added extra argument to microprocess, specifically tag=
          this allows the name of the microprocess to be tagged.
          This is useful in conjunction with WaitComplete and The
          Introspector and pausing to understand why a piece of
          code is staying in a particular WaitComplete loop/state.
        * When .stop() is called the microprocess, it's scheduler
          is set to a null scheduler.
        * Extra error messages when you call WaitComplete with a
          function rather than a generator. (you should only pass
          a generator object into WaitComplete, rather than a
          function).

    Index: Axon/Linkage.py
        * Documentation changed to REST format
        * Major documentation improvements.
        * Extra debugging provided in the case of trying to make a
          link from an outbox that doesn't exist. This is possible
          to do accidentally by having a trailing comma in the
          linkage description. (So this possible causes is
          described in the error message)

    Index: Axon/Ipc.py
        * Documentation changed to REST format
        * Major documentation improvements.
        * Signature of WaitComplete changed from:
           def __init__(self, *args):
           to 
           def __init__(self, *args,**argd):
           Copies of args/argd copied in as attributes. 

    Index: Axon/debugConfigFile.py
        * Documentation changed to REST format
        * Major documentation improvements.

    Index: Axon/util.py
        * Documentation changed to REST format
        * Documentation improvements.

    Index: Axon/Scheduler.py
        * Documentation changed to REST format
        * Major documentation improvements.
        * import os
        * Signature changed to include **argd rather than no args.
        * Added "wait_for_one" attribute
           - Means the scheduler can be started without any
             components/microprocesses being ready to run.
        * Added in a stopRequests queue (for safely recieving
          method calls from users of the system)
        * The wait_for_one class flag causes an internal flag to
          note that we have to wait for at least one microprocess
          to start before the scheduler exits.
        * New method waitForOne to allow the same flag to be set
        * This flag is cleared when a new microprocess is started.
        * listAllThreads method now switches on local debugging as
           well.
        * Handling of WaitComplete extended to allow passing
          through any tag provided by the user. Otherwise a default
          tag is created based on the parent's microprocess name.
        * Support for .stop() requests changes the logic in the
          main loop for the scheduler to allow clean shutdown and
          exit of loops. After exitting the main loop, the
          scheduler calls the .stop() method of all
          microprocesses & components in the run queue.
          One key use case for this is to allow clean close and
          shutdown of TCP sockets when someone calls
          self.scheduler.stop()
        * The self.stop() method however doesn't directly
          maniplate this flag, but in fact updates a threadsafe
          queue. The reason for that is to allow threaded
          components as well as generator components to cleanly
          call this method.

    Index: Axon/AdaptiveCommsComponent.py
        * Documentation changed to REST format
        * Major documentation improvements.
        * Change to _AdaptiveCommsable.__init__ signature to
          support class based system configuration.
        * addOutbox defaults to also ensuring that the
          self.unpause callback gets added as the notification
          callback when a message is removed from an outbox.
        * Change to AdaptiveCommsableComponent.__init__ signature
          to support class based system configuration.

    Index: Axon/CoordinatingAssistantTracker.py
        * Documentation changed to REST format
        * Major documentation improvements.
        * New .zap() method to clear the services and information
          logged by the co-ordinating assistant tracker. This was
          added to assist with multiple process support.

    Index: Axon/debug.py
        * Documentation changed to REST format
        * Documentation improvements.

    Index: Axon/idGen.py
        * Documentation changed to REST format
        * Documentation improvements.

    Index: setup.py
        * Annotated slightly to assist building targetted
          application tar balls.

    Index: CHANGELOG
    +
    +   * Added support for *basic* software transactional memory
    +    * Software transactional memory is a fancy phrase for something
    +      that boils down to something similar to version control for
    +      variables. You can checkout the current state, make modifications
    +      and try to commit them back. If the commit succeeds, you
    +      successfully updated it. If it doesn't, you didn't.
    +
    +      This implements it, and provides a mechanism for making the CAT
    +      safe for threads to use as well as standard components.
    +
    +    Added in LikeFile --> renamed to Handle
    +    Added in support for monkey patching the internals of a component
    +    system.

    +1.5.1 -> 1.x.x
    +    An exception is now raised if you try to create a linkage going
    +    from an inbox/outbox that already has a linkage going from it.
    +
    +    Waking up of producer components re-introduced (bugfix)
    +
    +    * When a component collects a message from an inbox; all producer
    +      components with outboxes linked to that inbox will be woken.
    +
    +    Additions to the Axon Test Suite providing test coverage of this
    +    facility.
