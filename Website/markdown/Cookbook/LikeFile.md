---
pagename: Cookbook/LikeFile
last-modified-date: 2008-09-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
    =================================================
    LikeFile - file-like interaction with components.
    =================================================

    LikeFile is a way to run Axon components with code that is not Axon-aware. It
    does this by running the scheduler and all associated microprocesses in a
    separate thread, and using a custom component to communicate if so desired.


    Using this code
    ---------------

    With a normal kamaelia system, you would start up a component and start
    running the Axon scheduler as follows, either:

        from Axon.Scheduler import scheduler
        component.activate()
        scheduler.run.runThreads()
        someOtherCode()

    or simply:

        component.run()
        someOtherCode()

    In both cases, someOtherCode() only run when the scheduler exits. What do you
    do if you want to (e.g.) run this alongside another external library that has
    the same requirement?

    Well, first we start the Axon scheduler in the background as follows:

        from likefile import schedulerThread
        schedulerThread().start()

    The scheduler is now actively running in the background, and you can start
    components on it from the foreground, in the same way as you would from inside
    kamaelia (don't worry, activate() is threadsafe):

        component.activate()
        someOtherCode()

    "component" will immediately start running and processing. This is fine if it's
    something non-interactive like a TCP server, but what do we do if we want to 
    interact with this component from someOtherCode?

    In this case, we use LikeFile, instead of activating. This is a wrapper
    which sits around a component and provides a threadsafe way to interact
    with it, whilst it is running in the backgrounded sheduler:

        from likefile import LikeFile
        wrappedComponent = LikeFile(component)
        someOtherCode()

    Now, wrappedComponent is an instance of the likefile wrapper, and you can
    interact with "component" by calling get() on wrappedComponent, to get data
    from the outbox on "component", or by calling put(data) to put "data" into
    the inbox of "component" like so:

        p = LikeFile( SimpleHTTPClient() )
        p.put("http://google.com")
        google = p.get()
        p.shutdown()
        print "google's homepage is", len(google), "bytes long.

    for both get() and put(), there is an optional extra parameter boxname,
    allowing you to interact with different boxes, for example to send a message
    with the text "RELOAD" to a component's control inbox, you would do:

        wrappedComponent.put("RELOAD", "control")
        wrappedComponent.get("signal")

    Finally, LikeFile objects have a shutdown() method that sends the usual Axon
    IPC shutdown messages to a wrapped component, and prevents further IO.


    Diagram of LikeFile's functionality
    -----------------------------------
    LikeFile is constructed from components like so:


         +----------------------------------+
         |             LikeFile             |
         +----------------------------------+
              |                      / \ 
              |                       |
          InQueues                 OutQueues
              |                       |
    +---------+-----------------------+---------+
    |        \ /                      |         |
    |    +---------+               +--------+   |
    |    |  Input  |   Shutdown    | Output |   |
    |    | Wrapper | ------------> |        |   |
    |    | (thread)|   Message     |Wrapper |   |
    |    +---------+               +--------+   |
    |         |                      / \        |
    |         |                       |         |
    |     Inboxes                 Outboxes      |
    |         |                       |         |
    |        \ /                      |         |
    |    +----------------------------------+   |
    |    |      the wrapped component       |   |
    |    +----------------------------------+   |
    |                                           |
    |    +----------------------------------+   |
    |    |       Some other component       |   | 
    |    |     that was only activated      |   |
    |    +----------------------------------+   |
    |                                           |
    |  AXON SCHEDULED COMPONENTS                |
    +-------------------------------------------+




    Note 1: Threadsafeness of activate().

    when a component is activated, it calls the method inherited from microprocess, which calls _addThread(self)
    on an appropriate scheduler. _addThread calls wakeThread, which places the request on a threadsafe queue.
