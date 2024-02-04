---
pagename: AxonHandle
last-modified-date: 2008-10-20
page-template: default
page-type: text/markdown
page-status: current|legacy|needsupdate|deprecated|recommended
---
Axon Component Handles
======================

The purpose behind Axon.Handle\'s is to allow the use of Kamaelia based
components and systems in non-Kamaelia systems, in a relatively
intuitive way.\

Premise
-------

The name **Handle** derives from the concept of a file-handle. We
dropped the name \"LikeFile\" since whilst it derives from the concept
of a file handle, it doesn\'t use the same API as file() for some good
reasons we\'ll come back to.\

A file handle is an opaque thing that you can *.write()* data to, and
*.read()* data from. This is a very simple concept and belies a huge
amount of parallel activity happening concurrently to your application.
The file system is taking your data and typically buffering it into
blocks. Those blocks then may need padding, and depending on the file
system, may actually be written immediately to the end of a cyclone
buffer in a journal with some write operations. Then periodically those
buffers get flushed to the actual disk.

Based on the fact that file handles are a very natural thing for people
to work with, based on their ubiquity, and the fact that it masks the
fact you\'re accessing a concurrent system from a linear one, that\'s
why we\'ve taken this approach for integrating Kamaelia components
(which are naturally parallel) with non-Kamaelia code, which is
typically not parallel.\

For simplicity of implementation, initially the implementation of Handle
supports only the equivalent of non-blocking file handles. This has two
implications:

-   Reading data from a Handle may fail, since there may not be any
    ready yet. This is chosen in preference to a blocking operation\
-   Writing data to a Handle may also fail, since the component may not
    actually be ready to receive data from us.\

Running the Axon Scheduler in the Background
--------------------------------------------

Clearly for this to work, Kamaelia\'s core - Axon - needs a way of
running components in the background. ie a way of putting the scheduler
in the background. This is actually pretty trivial, and can be used in a
very basic way (say, to run an Echo Protocol server in the background)
like this:\
\

>     from Axon.background import background
>
>     # Start the scheduler in a background thread
>     #
>     background().start()
>
>     # Add something to run in the background.
>     from Kamaelia.Protocol.EchoProtocol import EchoProtcol
>     from Kamaelia.Chassis.ConnectedServer import SimpleServer
>
>     # Due to background().start() above, the following starts running in
>     # the background immediately. 
>     SimpleServer(protocol=EchoProtcol, port=1500).activate()
>
>     # Do something else in the foreground.
>     import time
>     while 1:
>          time.sleep(1)
>          print "Ptang!"

As should be clear from this, the scheduler is started in the
background, the server is activated and then system sits waiting for
people to connect whilst periodically going \"Ptang!\"\

Example Component
-----------------

We\'ll use the following component in our examples below:

>     class Reverser(Axon.Component.component):
>         Inboxes = {
>              "inbox": "We receive data to reverse here",
>              "control": "We shutdown when a message is sent here"
>         }
>         Outboxes = {
>              "outbox": "We pass on the reversed message here",
>              "signal": "We pass on any shutdown message that we receive here."
>         }
>
>         def main(self):
>             while not self.dataReady("control):
>                 while self.dataReady('inbox'):
>                     item = self.recv('inbox')
>                     self.send(item[::-1], 'outbox') # reverse the string
>
>                 if not self.anyReady():
>                     self.pause()
>
>                 yield 1
>
>             self.send( self.recv("control), "signal" ) # pass on the shutdown

Now, clearly this is a simple component, but it be anything. If could
for example be a component that forwards each line to
translate.google.com or babelfish.av.com, to translate the provided
words into a different language. The usage would still be the same -
messages coming in inbox \"inbox\", and transformed data coming out
outbox \"outbox\".\

Usage
-----

Given the example component above, we decide to manually feed it the
contents of stdin.\

First of all we need our imports:\

>     from Axon.Handle import Handle
>
>     from Axon.background import background
>
>     import Queue

Queue is needed because currently the exceptions thrown by Handle (when
the Handle isn\'t ready) are from that module.\

Start the scheduler in the background:

>     background().start()

Start our Reverser component in the background, inside a Handle:

>     reverser = Handle(Reverser()).activate()

The it\'s just a matter of using it:

>     while True:
>         line = sys.stdin.readline()
>         if line == "":
>            break
>         line = line.rstrip() # get rid of newline - looks odd otherwise :)
>
>         reverser.put(line, "inbox")
>
>         while 1:
>             try:
>                 enil = reverser.get("outbox")
>                 break
>             except Queue.Empty:
>                 time.sleep(0.1)
>
>         print enil

What should be clear here is that we feed data into the reverser using
the .put() method.

The reason why we don\'t use a file-like object\[1\] here also becomes
clear : 1) unlike read()/write() we have multiple possible destinations
for the data - \"inbox\", \"control\", and we also have multiple sources
of data \"outbox\", \"signal\". 2) Also, rather than shipping over
binary data, we\'re passing over arbitrary python objects. Whilst in
this case this happens to be strings it could be anything from simple
records in dictionaries through to video data.\

> \[1\] ie using the file API of write/read

Other Examples
--------------

Other examples are in the Axon distribution and also in the Kamaelia
Distribution. These can be browsed online here:\

-   [Axon Handle
    Examples](http://code.google.com/p/kamaelia/source/browse/trunk/Code/Python/Axon/Examples/Handles/)
-   [Kamaelia Handle
    Examples](http://code.google.com/p/kamaelia/source/browse/trunk/Code/Python/Kamaelia/Examples/Handles/)

Limitations
-----------

Limitations:\

-   It currently will only allow access to components with the
    default/standard inboxes of inbox/control/signal/outbox.
-   This is a known limitation, but covers a wide class of situations.

\
